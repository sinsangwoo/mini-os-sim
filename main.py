import time
from process import Process, ProcessState
from scheduler import FCFS_Scheduler, SJF_Scheduler, RoundRobin_Scheduler, Priority_Scheduler
from cpu import CPU
from memory import Memory, MMU
from memory_manager import MemoryManager

def run_simulation(scheduler, job_list, max_time=20):
    # 주어진 스케줄러와 작업 목록으로 시뮬레이션을 수행하고 결과를 반환함
    print(f"\n시뮬레이션 시작 (Scheduler: {type(scheduler).__name__})")
    # CPU 준비
    cpu = CPU()
    # 전역 시간
    global_time = 0
    # 완료된 프로세스 기록용
    finished_processes = []
    # 1KB 만큼의 메모리
    ram = Memory(1024)
    # MMU
    mmu = MMU(ram)
    # 메모리 관리자
    cpu = CPU(mmu)
    # 메모리 관리자 준비
    mm = MemoryManager(ram)
    
    # job_list를 복사해서 사용 (원본 보존)
    pending_jobs = list(job_list)
    
    while global_time < max_time:
        # 순서 변경 실험: Execution을 먼저 하고 Arrival을 나중에 하면?
        print(f"\n[Time: {global_time:>2}] {'='*30}") 

        # 1. [Arrival]
        # 리스트 순회 시 삭제 문제가 발생하지 않도록 복사본이나 인덱스 관리 필요
        # 여기서는 pending_jobs의 복사본을 만들어 순회
        for p in list(pending_jobs): 
            if p.arrival_time == global_time:
                if mm.allocate(p):
                    # 성공하면 스케줄러에 등록
                    scheduler.add_process(p)
                    p.change_state(ProcessState.READY)
                    pending_jobs.remove(p)
                    print(f"   [Arrival] PID {p.pid} 도착 -> Ready Queue 등록")
                else:
                    # 실패하면? (OOM)
                    # 실제 OS는 스왑(Swap)을 쓰거나 OOM Killer를 부르지만,
                    # 여기선 일단 '대기'시키거나 '버림' 처리.
                    # 여기서는 '다음 틱에 다시 시도'하도록 놔둠 (pending_jobs에 유지)
                    print(f"   [Arrival Failed] PID {p.pid} 메모리 부족으로 대기 중...")
        # 2. [Scheduling]
        if not cpu.is_busy():
            next_process = scheduler.get_next_process()
            if next_process:
                cpu.load_process(next_process)
                next_process.change_state(ProcessState.RUNNING)
        
        # 3. [Execution]
        if cpu.is_busy():
            cpu.run()
            
            # 교체 중이면 패스
            if cpu.is_switching:
                continue
                
            current = cpu.current_process
            if current:
                # [28일 차 핵심] 처음 실행되는 순간인가?
                if current.first_run_time == -1:
                    current.first_run_time = global_time
                    # 응답 시간 = 처음 실행 시간 - 도착 시간
                    current.response_time = current.first_run_time - current.arrival_time
                    # 로그 출력 (선택)
                    print(f"   [Response] PID {current.pid} 첫 응답! (Response Time: {current.response_time})")

                print(f"   [Run] PID {current.pid} 실행 중 ...")
            
            # 3-1. 종료 검사 (우선순위 1등, 일 다 했으면 나가는 게 맞음)
            if current.remaining_time == 0:
                print(f"   [Done] PID {current.pid} 종료!")
                current.change_state(ProcessState.TERMINATED)
                current.turnaround_time = (global_time + 1) - current.arrival_time
                finished_processes.append(current)
                cpu.current_process = None 
                mm.deallocate(current)
            
            # 3-2. [25일 차 핵심] 타임 퀀텀 초과 검사 (Preemption)
            # 스케줄러가 RR이고, 현재 프로세스가 퀀텀만큼 실행했다면?
            elif isinstance(scheduler, RoundRobin_Scheduler):
                if cpu.cpu_burst_counter >= scheduler.time_quantum:
                    # 쫓겨나는 로그
                    print(f"   [Timeout] PID {current.pid} 타임 퀀텀({scheduler.time_quantum}) 초과! -> 강제 방출")
                    
                    # 1. 상태 변경 (Running -> Ready)
                    current.change_state(ProcessState.READY)
                    
                    # 2. 큐의 맨 뒤로 다시 줄 서기
                    scheduler.add_process(current)
                    
                    # 3. CPU 비우기 (다음 루프에서 스케줄러가 새 프로세스를 올림)
                    cpu.current_process = None 

        # 4. [Aging] 대기 시간 누적
        for p in scheduler.ready_queue:
            p.waiting_time += 1
            
        global_time += 1
        
        # 모든 작업이 완료되었고, 대기 중인 작업도 없으면 조기 종료
        if not pending_jobs and not cpu.is_busy() and not scheduler.ready_queue:
            print("\n모든 작업이 완료되어 시뮬레이션을 조기 종료합니다.")
            break
            
    return finished_processes

def print_report(finished_processes):
    print("\n" + "="*65) # 폭을 좀 넓힘
    print("[Final Report] 시뮬레이션 결과 통계")
    print("="*65)
    # Response 항목 추가
    print(f"{'PID':<5} | {'Arrival':<8} | {'Burst':<6} | {'Waiting':<8} | {'Turnaround':<10} | {'Response':<8}")
    print("-" * 65)
    
    total_waiting = 0
    total_turnaround = 0
    total_response = 0 # 추가
    
    finished_processes.sort(key=lambda x: x.pid)
    
    for p in finished_processes:
        print(f"{p.pid:<5} | {p.arrival_time:<8} | {p.burst_time:<6} | {p.waiting_time:<8} | {p.turnaround_time:<10} | {p.response_time:<8}")
        total_waiting += p.waiting_time
        total_turnaround += p.turnaround_time
        total_response += p.response_time # 추가
        
    print("-" * 65)
    count = len(finished_processes)
    if count > 0:
        print(f"평균 대기 시간 : {total_waiting / count:.2f}")
        print(f"평균 반환 시간 : {total_turnaround / count:.2f}")
        print(f"평균 응답 시간 : {total_response / count:.2f}") # 추가
    else:
        print("완료된 프로세스가 없습니다.")
    print("="*65)

def main():
    print("--- 🖥️  Mini OS Simulator: MMU Test ---")
    
    # 1. 하드웨어 준비
    ram = Memory(1024)
    mmu = MMU(ram)
    
    # 2. 프로세스 생성
    p1 = Process(0, 10)
    
    # 3. 수동 매핑 (OS가 해줬다고 가정)
    # p1의 0번 페이지 -> 실제 5번 프레임 (20~23번지)
    # p1의 1번 페이지 -> 실제 2번 프레임 (8~11번지)
    p1.page_table[0] = 5
    p1.page_table[1] = 2
    
    print(f"\n[Setup] PID 1 Page Table: {p1.page_table}")
    
    # 4. 주소 변환 테스트
    # Case 1: VA 0번지 (VPN 0, Offset 0) -> PA 20번지 예상
    pa = mmu.translate(p1, 0)
    print(f"[Test 1] VA 0 -> PA {pa} (기대값: 20)")
    
    # Case 2: VA 2번지 (VPN 0, Offset 2) -> PA 22번지 예상
    pa = mmu.translate(p1, 2)
    print(f"[Test 2] VA 2 -> PA {pa} (기대값: 22)")
    
    # Case 3: VA 5번지 (VPN 1, Offset 1) -> PA 9번지 예상 (2*4 + 1)
    pa = mmu.translate(p1, 5)
    print(f"[Test 3] VA 5 -> PA {pa} (기대값: 9)")
    
    # Case 4: VA 100번지 (매핑 안 됨) -> Page Fault 예상
    pa = mmu.translate(p1, 100)
    print(f"[Test 4] VA 100 -> PA {pa} (기대값: -1)")

if __name__ == "__main__":
    main()
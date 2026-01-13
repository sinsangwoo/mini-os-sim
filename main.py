import time
from process import Process, ProcessState
from scheduler import FCFS_Scheduler
from cpu import CPU

def main():
    print("--- 🖥️  Mini OS Simulator Booting... ---")
    
    scheduler = FCFS_Scheduler()
    cpu = CPU()
    global_time = 0
    
    # [분석용 시나리오]
    JOB_LIST = [
        Process(arrival_time=0, burst_time=10), # P1
        Process(arrival_time=1, burst_time=1),  # P2
        Process(arrival_time=2, burst_time=1)   # P3
    ]
    
    # 나중에 통계를 내기 위해 완료된 프로세스들을 모아둘 리스트
    finished_processes = []
    
    MAX_TIME = 20
    
    while global_time < MAX_TIME:
        # ... (기존 로그 출력 및 Arrival 로직 동일) ...
        print(f"\n[Time: {global_time:>2}] {'='*30}") 

        # 1. [Arrival]
        for p in list(JOB_LIST): 
            if p.arrival_time == global_time:
                scheduler.add_process(p)
                p.change_state(ProcessState.READY)
                JOB_LIST.remove(p)
                print(f"   ✨ [Arrival] PID {p.pid} 도착")

        # 2. [Scheduling]
        if not cpu.is_busy():
            next_process = scheduler.get_next_process()
            if next_process:
                cpu.load_process(next_process)
                next_process.change_state(ProcessState.RUNNING)
        
        # 3. [Execution]
        if cpu.is_busy():
            cpu.run()
            current = cpu.current_process
            print(f"   ⚙️  [Run] PID {current.pid} 실행 중 | RT: {current.remaining_time}")
            
            if current.remaining_time == 0:
                print(f"   🎉 [Done] PID {current.pid} 종료!")
                current.change_state(ProcessState.TERMINATED)
                
                # [19일 차 추가] 반환 시간(Turnaround Time) 계산
                # TT = 완료 시간 - 도착 시간
                # 완료 시간 = 현재 시간 + 1 (이번 틱까지 실행했으므로)
                current.turnaround_time = (global_time + 1) - current.arrival_time
                
                # 통계용 리스트에 저장
                finished_processes.append(current)
                
                cpu.current_process = None 

        # === [19일 차 핵심] 대기 시간 누적 (Aging) ===
        # Ready Queue에 있는 모든 프로세스에게 "너네 1초 더 기다렸다"고 기록
        for p in scheduler.ready_queue:
            p.waiting_time += 1
            
        global_time += 1
        # time.sleep(0.1)

    # === [최종 성적표 출력] ===
    print("\n" + "="*50)
    print("📊 [Final Report] 시뮬레이션 결과 통계")
    print("="*50)
    print(f"{'PID':<5} | {'Arrival':<8} | {'Burst':<6} | {'Waiting':<8} | {'Turnaround':<10}")
    print("-" * 50)
    
    total_waiting = 0
    total_turnaround = 0
    
    # PID 순서대로 정렬해서 출력
    finished_processes.sort(key=lambda x: x.pid)
    
    for p in finished_processes:
        print(f"{p.pid:<5} | {p.arrival_time:<8} | {p.burst_time:<6} | {p.waiting_time:<8} | {p.turnaround_time:<10}")
        total_waiting += p.waiting_time
        total_turnaround += p.turnaround_time
        
    print("-" * 50)
    avg_waiting = total_waiting / len(finished_processes) if finished_processes else 0
    avg_turnaround = total_turnaround / len(finished_processes) if finished_processes else 0
    
    print(f"👉 평균 대기 시간 (Avg Waiting Time): {avg_waiting:.2f}")
    print(f"👉 평균 반환 시간 (Avg Turnaround Time): {avg_turnaround:.2f}")
    print("="*50)

if __name__ == "__main__":
    main()
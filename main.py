import time
from process import Process, ProcessState
from scheduler import FCFS_Scheduler
from cpu import CPU
from memory import Memory, MMU
from memory_manager import MemoryManager

def run_simulation(scheduler, job_list, max_time=30):
    print(f"\n 시뮬레이션 시작 (Scheduler: {type(scheduler).__name__})")
    
    # 하드웨어 초기화 
    ram = Memory(32) 
    mmu = MMU(ram)
    cpu = CPU(mmu)
    mm = MemoryManager(ram)
    
    global_time = 0
    finished_processes = []
    waiting_queue = []
    pending_jobs = list(job_list)
    
    # 시뮬레이션 루프. global_time이 max_time에 도달하거나 모든 프로세스가 종료될 때까지 반복
    while global_time < max_time:
        print(f"\n[Time: {global_time:>2}] {'='*30}") 
        ram.print_map()
        # [Arrival & Allocation]
        for p in list(pending_jobs): 
            if p.arrival_time == global_time:
                # 메모리 할당 (LRU 교체 포함)
                if mm.allocate(p):
                    scheduler.add_process(p)
                    p.change_state(ProcessState.READY)
                    pending_jobs.remove(p)
                    print(f"   [Arrival] PID {p.pid} 도착 -> Ready Queue 등록")
                else:
                    print(f"   [Arrival Failed] PID {p.pid} 메모리 부족 (OOM)")

        # [Scheduling]
        if not cpu.is_busy():
            next_process = scheduler.get_next_process()
            if next_process:
                cpu.load_process(next_process)
                next_process.change_state(ProcessState.RUNNING)
        
        # [Execution]
        if cpu.is_busy():
            cpu.run()
            
            if cpu.is_switching:
                global_time += 1
                continue

            current = cpu.current_process
            if current:
                # 만약 page fault가 나서 page_falut_flag가 True로 설정되었다면
                # 현재 프로세스를 대기 상태로 전환하고 CPU에서 제거하여 다음 사이클에 다른 프로세스를 실행하도록 함
                if cpu.page_fault_flag:
                    print(f"   [OS] Handling Page Fault for PID {current.pid} -> Blocked")
                    # 상태 변경 (Running -> Waiting)
                    current.change_state(ProcessState.WAITING)
                    
                    # 대기 큐로 이동
                    waiting_queue.append(current)
                    
                    # CPU 비우기 (Context Switch 유발)
                    cpu.current_process = None
                    
                    # 이번 틱은 여기서 종료 (종료 검사 안 함)
                    pass
                else:
                    # 정상 실행 시 로그 및 종료 검사
                    print(f"   [Run] PID {current.pid} 실행 중 | RT: {current.remaining_time}")
                    
                    if current.remaining_time == 0:
                        print(f"   [Done] PID {current.pid} 종료!")
                        current.change_state(ProcessState.TERMINATED)
                        current.turnaround_time = (global_time + 1) - current.arrival_time
                        finished_processes.append(current)
                        mm.deallocate(current)
                        cpu.current_process = None 
                
                if current.remaining_time == 0:
                    print(f"   [Done] PID {current.pid} 종료!")
                    current.change_state(ProcessState.TERMINATED)
                    current.turnaround_time = (global_time + 1) - current.arrival_time
                    finished_processes.append(current)
                    
                    # 메모리 반납
                    mm.deallocate(current)
                    cpu.current_process = None 

        # 4. [Aging]
        for p in scheduler.ready_queue:
            p.waiting_time += 1
            
        global_time += 1
        
        if not pending_jobs and not cpu.is_busy() and not scheduler.ready_queue and not waiting_queue:
            print("\n조기 종료")
            break
            
    return finished_processes

def main():
    print("---   Mini OS Simulator: Memory Visualization ---")
    
    # [시나리오]
    # RAM: 총 8프레임
    # P1(4프레임 필요): 0초 도착, 3초 실행 -> 0~3 프레임 차지
    # P2(4프레임 필요): 1초 도착, 3초 실행 -> 4~7 프레임 차지 (RAM 꽉 참!)
    # P3(4프레임 필요): 2초 도착, 3초 실행 -> OOM 발생! (LRU 교체 발생)
    
    jobs = [
        Process(arrival_time=0, burst_time=3),
        Process(arrival_time=1, burst_time=3),
        Process(arrival_time=2, burst_time=3)
    ]
    
    run_simulation(FCFS_Scheduler(), jobs)

if __name__ == "__main__":
    main()
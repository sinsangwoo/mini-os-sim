import time
from process import Process, ProcessState
from scheduler import FCFS_Scheduler
from cpu import CPU
from memory import Memory, MMU
from memory_manager import MemoryManager

def run_simulation(scheduler, job_list, max_time=30):
    print(f"\n 시뮬레이션 시작 (Scheduler: {type(scheduler).__name__})")
    
    # 하드웨어 초기화 (메모리 16바이트 = 4프레임)
    ram = Memory(16) 
    mmu = MMU(ram)
    cpu = CPU(mmu)
    mm = MemoryManager(ram)
    
    global_time = 0
    finished_processes = []
    pending_jobs = list(job_list)
    
    while global_time < max_time:
        print(f"\n[Time: {global_time:>2}] {'='*30}") 

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
                print(f"   [Run] PID {current.pid} 실행 중 | RT: {current.remaining_time}")
                
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
        
        if not pending_jobs and not cpu.is_busy() and not scheduler.ready_queue:
            print("\n조기 종료")
            break
            
    return finished_processes

def main():
    print("--- Mini OS Simulator: LRU Test ---")
    
    # P1: 0초 도착, 5초 실행
    # P2: 2초 도착, 5초 실행 (메모리 부족 유발 -> P1 페이지 쫓아냄)
    jobs = [
        Process(arrival_time=0, burst_time=5),
        Process(arrival_time=2, burst_time=5)
    ]
    
    run_simulation(FCFS_Scheduler(), jobs)

if __name__ == "__main__":
    main()
import time
from process import Process, ProcessState
from scheduler import FCFS_Scheduler
from cpu import CPU
from memory import Memory, MMU
from memory_manager import MemoryManager
from io_device import IODevice 

def run_simulation(scheduler, job_list, max_time=30):
    print(f"\n 시뮬레이션 시작 (Scheduler: {type(scheduler).__name__})")
    
    # 하드웨어 초기화 
    ram = Memory(32) 
    mmu = MMU(ram)
    cpu = CPU(mmu)
    mm = MemoryManager(ram)
    disk = IODevice("Disk")
    
    global_time = 0
    finished_processes = []
    pending_jobs = list(job_list)
    
    # 기존의 범용 wait_queue는 SLEEP 등을 위해 남겨둘 수도 있지만, 
    # 일단은 I/O 처리를 disk 객체에 전담시킴
    sleep_queue = [] # 나중에 SLEEP 시스템 콜을 위해 이름 변경
    
    while global_time < max_time:
        print(f"\n[Time: {global_time:>2}] {'='*30}") 
        ram.print_map() 

        # [Hardware Tick] I/O 디바이스 동작
        # CPU와 무관하게 디스크는 매 틱마다 돌아감
        disk.tick()

        # [Interrupt Handling] I/O 완료 인터럽트 처리
        # 디스크 작업이 끝난 프로세스가 있다면 깨워서 Ready Queue로 보냄
        while disk.finished_queue:
            proc = disk.finished_queue.pop(0)
            print(f"    [OS] I/O 완료 인터럽트 수신 -> PID {proc.pid} Ready Queue 복귀")
            proc.change_state(ProcessState.READY)
            scheduler.add_process(proc)

        # [Arrival & Allocation]
        for p in list(pending_jobs): 
            if p.arrival_time == global_time:
                if mm.allocate(p):
                    scheduler.add_process(p)
                    p.change_state(ProcessState.READY)
                    pending_jobs.remove(p)
                    print(f"    [Arrival] PID {p.pid} 도착 -> Ready Queue 등록")
                else:
                    print(f"    [Arrival Failed] PID {p.pid} 메모리 부족 (OOM)")

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
                # [시스템 콜 처리]
                if cpu.trap_flag:
                    sys_type, sys_arg = cpu.trap_cause
                    print(f"    [Syscall] PID {current.pid} requested '{sys_type}' for {sys_arg} ticks.")
                    
                    if sys_type == "EXIT":
                        print(f"    [Done] PID {current.pid} 정상 종료!")
                        current.change_state(ProcessState.TERMINATED)
                        current.turnaround_time = (global_time + 1) - current.arrival_time
                        finished_processes.append(current)
                        mm.deallocate(current)
                        cpu.current_process = None
                        
                    elif sys_type == "IO":
                        # OS가 직접 카운트하지 않고 I/O 디바이스에 넘김
                        print(f"    [Block] PID {current.pid} -> Disk 대기열로 이동")
                        current.change_state(ProcessState.WAITING)
                        disk.request_io(current, sys_arg) # 디바이스에 요청
                        cpu.current_process = None
                        
                    elif sys_type == "SLEEP":
                        # SLEEP은 I/O 장치를 안 쓰므로 OS가 직접 관리 (기존 로직 유지)
                        current.change_state(ProcessState.WAITING)
                        sleep_queue.append([current, sys_arg])
                        cpu.current_process = None
                        
                    global_time += 1
                    continue
                
                # [페이지 폴트 처리]
                if cpu.page_fault_flag:
                    print(f"    [OS] Handling Page Fault for PID {current.pid} -> Blocked")
                    current.change_state(ProcessState.WAITING)
                    # 실제로는 디스크에서 페이지를 가져오는 I/O 요청을 해야 하지만, 
                    # 시뮬레이션 단순화를 위해 일단 sleep_queue에 1틱 대기로 넣습니다.
                    sleep_queue.append([current, 1]) 
                    cpu.current_process = None
                    global_time += 1
                    continue
                
                print(f"     [Run] PID {current.pid} 실행 중 | 남은 CPU: {current.remaining_time}")

        # 5. [SLEEP Queue 처리] (기존에 작성하신 로직 활용)
        for entry in list(sleep_queue):
            proc, remaining = entry
            remaining -= 1
            entry[1] = remaining
            if remaining <= 0:
                print(f"    [Wakeup] PID {proc.pid} 수면/폴트 대기 완료 -> Ready Queue 복귀")
                proc.change_state(ProcessState.READY)
                scheduler.add_process(proc)
                sleep_queue.remove(entry)

        # 6. [Aging]
        for p in scheduler.ready_queue:
            p.waiting_time += 1
            
        global_time += 1
        
        # 종료 조건 업데이트: pending_jobs, cpu, scheduler, disk, sleep_queue 모두 비어야 함
        if not pending_jobs and not cpu.is_busy() and not scheduler.ready_queue and not disk.is_busy() and not sleep_queue and not disk.finished_queue:
            print("\n 모든 작업이 완료되어 시뮬레이션을 조기 종료합니다.")
            break
            
    return finished_processes

def main():
    print("---   Mini OS Simulator: I/O Device Modeling ---")
    
    # [시나리오]
    # P1: CPU 2초 -> I/O 5초 -> CPU 2초
    # P2: CPU 10초 (P1이 I/O 하는 동안 P2가 CPU를 독점해야 함!)
    jobs = [
        Process(arrival_time=0, behavior=[("CPU", 2), ("IO", 5), ("CPU", 2)]),
        Process(arrival_time=1, behavior=[("CPU", 10)]) 
    ]
    
    run_simulation(FCFS_Scheduler(), jobs, max_time=30)

if __name__ == "__main__":
    main()
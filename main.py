import time
from process import Process, ProcessState
from scheduler import FCFS_Scheduler, RoundRobinScheduler
from cpu import CPU
from memory import Memory, MMU
from memory_manager import MemoryManager
from io_device import IODevice

def run_simulation(scheduler, job_list, max_time=30):
    print(f"\n 시뮬레이션 시작 (Scheduler: {type(scheduler).__name__})")
    
    ram = Memory(32) 
    mmu = MMU(ram)
    cpu = CPU(mmu)
    mm = MemoryManager(ram)
    disk = IODevice("Disk")
    
    global_time = 0
    finished_processes = []
    pending_jobs = list(job_list)
    
    # OS가 직접 관리하는 타이머 대기열
    sleep_queue = [] 
    
    while global_time < max_time:
        print(f"\n[Time: {global_time:>2}] {'='*30}") 

        # [Hardware Tick]
        disk.tick()

        # [Interrupt Handling] I/O 완료
        while disk.finished_queue:
            proc = disk.finished_queue.pop(0)
            print(f"   ⚡ [OS] I/O 완료 인터럽트 수신 -> PID {proc.pid} Ready Queue 복귀")
            proc.change_state(ProcessState.READY)
            scheduler.add_process(proc)

        # [Timer Handling] SLEEP 완료 처리
        # sleep_queue에 있는 녀석들의 시간을 1씩 줄이고, 0이 되면 깨움
        # 리스트를 순회하며 삭제할 때는 복사본(list())을 사용해야 안전함
        for entry in list(sleep_queue):
            proc, remaining_sleep = entry
            remaining_sleep -= 1
            # 남은 수면 시간이 업데이트된 값을 반영하도록 entry를 수정
            entry[1] = remaining_sleep 
            
            if remaining_sleep <= 0:
                print(f"    [OS] 타이머 알람! PID {proc.pid} 수면 완료 -> Ready Queue 복귀")
                proc.change_state(ProcessState.READY)
                scheduler.add_process(proc)
                sleep_queue.remove(entry)

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
                        print(f"    [Syscall] PID {current.pid} requested 'EXIT'. 정상 종료 처리 중...")
                        # terminated로 상태 변경
                        current.change_state(ProcessState.TERMINATED)
                        # 종료 시간 계산
                        current.turnaround_time = (global_time + 1) - current.arrival_time
                        finished_processes.append(current)
                        # 자원 반납
                        mm.deallocate(current)
                        # cpu에서 제거
                        cpu.current_process = None
                        
                    elif sys_type == "IO":
                        print(f"    [Block] PID {current.pid} -> Disk 대기열로 이동")
                        current.change_state(ProcessState.WAITING)
                        disk.request_io(current, sys_arg) 
                        cpu.current_process = None
                        
                    elif sys_type == "SLEEP":
                        # SLEEP 시스템 콜 처리
                        print(f"    [Block] PID {current.pid} -> Sleep Queue로 이동 ({sys_arg}틱 대기)")
                        current.change_state(ProcessState.WAITING)
                        sleep_queue.append([current, sys_arg])
                        cpu.current_process = None
                    
                    # FORK 시스템 콜 처리
                    elif sys_type == "FORK":
                        child_process = current.clone(global_time)
                        
                        # 자식에게 메모리 할당 (실패하면 FORK 실패 처리해야 하지만, 여기선 성공 가정)
                        if mm.allocate(child_process):
                            # 자식을 Ready Queue에 넣음
                            child_process.change_state(ProcessState.READY)
                            scheduler.add_process(child_process)
                            print(f"    [OS] 자식 프로세스(PID {child_process.pid}) Ready Queue 등록 완료")
                        else:
                            print(f"    [OS] 메모리 부족으로 FORK 실패 (PID {child_process.pid} 파기)")
                            # 실패 처리 로직 (생략)

                        # FORK는 I/O나 SLEEP과 달리 부모를 대기(Block)시키지 않음
                        # 부모는 계속해서 CPU를 쓸 수 있음 (물론 RR이라면 퀀텀에 따라 쫓겨날 순 있음)
                        # 따라서 cpu.current_process = None을 하지 않고 그대로 둠
                        
                    global_time += 1
                    continue
                
                # [페이지 폴트 처리]
                if cpu.page_fault_flag:
                    print(f"    [OS] Handling Page Fault for PID {current.pid} -> Blocked")
                    current.change_state(ProcessState.WAITING)
                    # (임시) 페이지 폴트가 발생하면 1틱 동안 대기 후 Ready Queue로 복귀하는 시뮬레이션
                    sleep_queue.append([current, 1]) 
                    cpu.current_process = None
                    global_time += 1
                    continue
                
                print(f"     [Run] PID {current.pid} 실행 중 | 남은 CPU: {current.remaining_time}")

        # [Aging]
        for p in scheduler.ready_queue:
            p.waiting_time += 1
            
        global_time += 1
        
        # 모든 작업이 완료된 경우 시뮬레이션 조기 종료
        if not pending_jobs and not cpu.is_busy() and not scheduler.ready_queue and not disk.is_busy() and not sleep_queue and not disk.finished_queue:
            print("\n 모든 작업이 완료되어 시뮬레이션을 조기 종료합니다.")
            break
            
    return finished_processes

def main():
    print("--- 🖥️  Mini OS Simulator: Graceful EXIT ---")
    
    # [시나리오]
    # 아주 단순한 프로세스 하나만 넣어서, 끝날 때 EXIT 시스템 콜이 잘 불리는지 확인
    jobs = [
        Process(arrival_time=0, behavior=[("CPU", 2)])
    ]
    
    run_simulation(FCFS_Scheduler(), jobs, max_time=10)

if __name__ == "__main__":
    main()
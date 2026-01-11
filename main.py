import time
from process import Process, ProcessState
from scheduler import FCFS_Scheduler
from cpu import CPU

def main():
    print("--- 🖥️  Mini OS Simulator Booting... ---")
    
    scheduler = FCFS_Scheduler()
    cpu = CPU()
    global_time = 0
    
    JOB_LIST = [
        # convoy effect 유도, 긴 작업이 먼저 도착하도록 설정   
        Process(arrival_time=0, burst_time=10),
        Process(arrival_time=1, burst_time=1),
        Process(arrival_time=2, burst_time=1)
    ]
    
    MAX_TIME = 20
    
    print(f"✅ 시스템 초기화 완료. (총 {len(JOB_LIST)}개의 작업 대기 중)\n")
    
    while global_time < MAX_TIME:
        print(f"\n[Time: {global_time:>2}] {'='*30}") 
        
        # 1. [Arrival]
        for p in list(JOB_LIST): 
            if p.arrival_time == global_time:
                scheduler.add_process(p)
                p.change_state(ProcessState.READY)
                JOB_LIST.remove(p)
                print(f"   ✨ [Arrival] PID {p.pid} 도착 (Ready Queue: {len(scheduler.ready_queue)})")

        # 2. [Scheduling]
        if not cpu.is_busy():
            next_process = scheduler.get_next_process()
            if next_process:
                cpu.load_process(next_process)
                next_process.change_state(ProcessState.RUNNING)
            else:
                print(f"   💤 [Idle] 대기 중인 프로세스 없음 (Ready Queue: {len(scheduler.ready_queue)})")

        # 3. [Execution]
        if cpu.is_busy():
            cpu.run()
            current = cpu.current_process
            print(f"   ⚙️  [Run] PID {current.pid} 실행 중 | 남은 시간: {current.remaining_time:>2} | PC: {current.registers['PC']}")
            
            if current.remaining_time == 0:
                print(f"   🎉 [Done] PID {current.pid} 종료! -> 자원 반납")
                current.change_state(ProcessState.TERMINATED)
                cpu.current_process = None 
            
        global_time += 1
        time.sleep(0.5) 

    print("\n--- 🛑 시뮬레이션 종료 ---")


if __name__ == "__main__":
    main()
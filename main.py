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
        Process(arrival_time=1, burst_time=3),
        Process(arrival_time=3, burst_time=5),
        Process(arrival_time=7, burst_time=2)
    ]
    
    MAX_TIME = 15
    
    print(f"✅ 시스템 초기화 완료. (총 {len(JOB_LIST)}개의 작업 대기 중)\n")
    
    while global_time < MAX_TIME:
        # [로그 개선 1] 시간 출력 포맷을 깔끔하게
        # end=""를 써서 줄바꿈을 안 하고, 뒤에 이어지는 로그들이 한 덩어리로 보이게 할 수도 있음.
        # 여기서는 그냥 헤더처럼 출력.
        print(f"\n[Time: {global_time:>2}] {'='*40}") 
        
        # 1. [Arrival]
        for p in list(JOB_LIST): 
            if p.arrival_time == global_time:
                scheduler.add_process(p)
                p.change_state(ProcessState.READY)
                JOB_LIST.remove(p)
                # [로그 개선 2] 이모지와 정렬 사용
                print(f"   ✨ [Arrival] PID {p.pid} 도착 (Ready Queue: {len(scheduler.ready_queue)})")

        # 2. [Scheduling]
        if not cpu.is_busy():
            next_process = scheduler.get_next_process()
            if next_process:
                cpu.load_process(next_process)
                next_process.change_state(ProcessState.RUNNING)
                # load_process 안에서 Context Switch 로그가 찍히므로 여기선 생략 가능
            else:
                # [로그 개선 3] IDLE 상태일 때도 큐 상태를 보여줌
                print(f"   💤 [Idle] 대기 중인 프로세스 없음 (Ready Queue: {len(scheduler.ready_queue)})")

        # 3. [Execution]
        if cpu.is_busy():
            cpu.run()
            current = cpu.current_process
            
            # [로그 개선 4] 실행 중인 프로세스 정보를 한 줄로 요약
            # Process.__repr__을 활용해도 좋음
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
import time
from process import Process, ProcessState
from scheduler import FCFS_Scheduler
from cpu import CPU

def main():
    print("--- Mini OS Simulator Booting... ---")
    
    scheduler = FCFS_Scheduler()
    cpu = CPU()
    global_time = 0
    
    JOB_LIST = [
        Process(arrival_time=1, burst_time=3),
        Process(arrival_time=3, burst_time=5),
        Process(arrival_time=7, burst_time=2)
    ]
    
    MAX_TIME = 20 # 넉넉하게 늘림
    
    print(f"시스템 초기화 완료. (총 {len(JOB_LIST)}개의 작업 대기 중)\n")
    
    while global_time < MAX_TIME:
        print(f"\n[Time: {global_time}] ------------------------------------")
        
        # [Arrival] 프로세스 도착 처리
        for p in list(JOB_LIST): 
            if p.arrival_time == global_time:
                scheduler.add_process(p)
                p.change_state(ProcessState.READY)
                JOB_LIST.remove(p)
                print(f"✨ [Arrival] PID {p.pid} 도착 -> Ready Queue 등록")

        # [Scheduling] CPU가 놀고 있으면 다음 타자 섭외
        if not cpu.is_busy():
            # 스케줄러에게 "다음 누구?" 물어봄
            next_process = scheduler.get_next_process()
            
            if next_process:
                # 대기자가 있으면 CPU에 올림 (Dispatch)
                cpu.load_process(next_process)
                
                # 상태 변경 (Ready -> Running)
                # [중요] CPU에 올라가는 순간 상태를 바꿔줌
                next_process.change_state(ProcessState.RUNNING)
            else:
                # 대기자도 없으면 그냥 놂
                print("   (IDLE) 대기 중인 프로세스가 없습니다.")

        # [Execution] CPU 실행
        if cpu.is_busy():
            cpu.run()
            # 현재 누구 실행 중인지 로그 출력
            print(f"   [Running] PID {cpu.current_process.pid} (남은 시간: {cpu.current_process.remaining_time})")
            
            # (내일 할 일: 다 끝났으면 종료 처리하는 로직이 여기에 필요함)
            # 지금은 종료 로직이 없어서 남은 시간이 -1, -2... 계속 내려감
            
        global_time += 1
        time.sleep(0.5)

    print("\n--- 🛑 시뮬레이션 종료 ---")

if __name__ == "__main__":
    main()
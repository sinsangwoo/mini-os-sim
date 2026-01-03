import time
from process import Process, ProcessState
from scheduler import FCFS_Scheduler
from cpu import CPU

def main():
    print("--- Mini OS Simulator Booting... ---")
    
    scheduler = FCFS_Scheduler()
    cpu = CPU()
    global_time = 0
    
    # 아직 시스템에 들어오지 않은 프로세스들
    # (도착 시간, 실행 시간)
    JOB_LIST = [
        Process(arrival_time=1, burst_time=3),
        Process(arrival_time=3, burst_time=5),
        Process(arrival_time=7, burst_time=2)
    ]
    
    # 시뮬레이션 종료 조건: 모든 작업이 끝나면 종료하고 싶지만, 
    # 일단은 넉넉하게 15초로 잡음
    MAX_TIME = 15
    
    print(f"시스템 초기화 완료. (총 {len(JOB_LIST)}개의 작업 대기 중)\n")
    
    while global_time < MAX_TIME:
        print(f"\n[Time: {global_time}] ------------------------------------")
        
        # === 프로세스 도착 처리 (Arrival) ===
        # JOB_LIST에 있는 녀석들 중, 지금 시간에 도착해야 할 녀석이 있나?
        
        # 리스트를 복사해서 돌리는 이유는 루프 도중 원본 리스트에서 요소를 삭제하면 꼬이기 때문.
        for p in list(JOB_LIST): 
            if p.arrival_time == global_time:
                # 스케줄러에 등록
                scheduler.add_process(p)
                
                # 상태 변경 (New -> Ready)
                p.change_state(ProcessState.READY) 
                
                # Job List에서 제거 (이제 시스템 안으로 들어왔으니)
                JOB_LIST.remove(p)
                
                print(f"[Arrival] 프로세스 도착! -> PID {p.pid}가 Ready Queue에 들어감.")

        # === CPU 실행 로직 (아직 스케줄링 연결 안 함) ===
        if cpu.is_busy():
            cpu.run()
        else:
            print("   (IDLE) 대기 중...")
            
        global_time += 1
        time.sleep(0.5)

    print("\n--- 시뮬레이션 종료 ---")

if __name__ == "__main__":
    main()
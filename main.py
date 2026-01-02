import time
from process import Process
from scheduler import FCFS_Scheduler
from cpu import CPU

def main():
    print("--- Mini OS Simulator Booting... ---")
    
    # 핵심 부품 초기화. 쉽게말해, OS의 주요 컴포넌트들을 준비함
    scheduler = FCFS_Scheduler()
    cpu = CPU()
    
    # 전역 시간 초기화
    global_time = 0
    
    # 종료 조건 설정을 위한 목표 시간. 지금은 10초로 설정
    MAX_TIME = 10
    
    print(f"시스템 초기화 완료. 시뮬레이션을 {MAX_TIME}초간 진행합니다.\n")
    
    # [커널 메인 루프]
    while global_time < MAX_TIME:
        print(f"\n[Time: {global_time}] ------------------------------------")
        
        # (나중에 여기에 프로세스 도착, 스케줄링 로직이 들어갈 것)
        # 지금은 아무것도 안 하고 시간만 흐름
        
        # CPU 실행 (현재 프로세스가 있다면 1틱 실행)
        if cpu.is_busy():
            cpu.run()
        else:
            print("   (IDLE) CPU가 할 일이 없어서 놉니다.")
            
        # 시간 증가
        global_time += 1
        
        # 속도 조절 (너무 빠르면 눈으로 못 보니까 0.5초 대기)
        time.sleep(0.5)

    print("\n--- 시뮬레이션 종료 (Max Time Reached) ---")

if __name__ == "__main__":
    main()
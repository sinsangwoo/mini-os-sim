# main.py, 앞으로 커널 역할을 할 메인 파일
from process import Process
from scheduler import Scheduler
from cpu import CPU

def main():
    print("--- Mini OS Simulator: Phase 2 Ready ---")
    
    # 앞으로 여기에 FCFS 스케줄러와 CPU를 생성하고 연결할 예정
    # scheduler = FCFSScheduler()
    # cpu = CPU()
    
    print("시스템 모듈(Process, Scheduler, CPU) 로드 완료.")
    print("이제 2단계: FCFS 스케줄러 구현을 시작할 준비가 되었습니다.")

if __name__ == "__main__":
    main()
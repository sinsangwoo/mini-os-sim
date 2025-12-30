from process import Process
from scheduler import FCFS_Scheduler

from process import Process
from cpu import CPU

def main():
    print("--- [12일 차] CPU 문맥 교환 테스트 ---")
    
    # CPU 생성
    cpu = CPU()
    print("CPU 초기화 완료")
    
    # 프로세스 2개 생성
    p1 = Process(0, 3) # PID 1
    p2 = Process(1, 5) # PID 2
    
    # 아무것도 없을 때 P1 로드
    print("\n[Scenario 1] CPU가 비어있을 때 P1을 로드합니다.")
    cpu.load_process(p1) # 기대 로그: None -> PID 1
    
    # P1을 조금 실행시킴
    print("\n[Scenario 2] P1을 1틱 실행합니다.")
    cpu.run()
    print(f"   -> P1 상태: {p1}") # PC가 1 증가했는지 확인
    
    # P1이 있는데 강제로 P2를 로드 (문맥 교환 발생)
    print("\n[Scenario 3] P1 실행 중에 P2로 교체합니다 (Context Switch).")
    cpu.load_process(p2) # 기대 로그: PID 1 -> PID 2
    
    # P2 실행
    print("\n[Scenario 4] P2를 1틱 실행합니다.")
    cpu.run()
    print(f"   -> P2 상태: {p2}")

    print("\n--- 테스트 종료 ---")

if __name__ == "__main__":
    main()
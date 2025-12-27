from process import Process, ProcessState
import random

def main():
    print("--- [CPU 실행 시작] ---\n")

     # 1. [탄생] 프로세스 생성 (실행 시간 3초짜리)
    p1 = Process(arrival_time=0, burst_time=3)
    print(f"\n [1. New] 프로세스 탄생: {p1}")
    
    # 2. [입장] 준비 큐로 이동
    print("\n [2. Admission] 준비 큐에 줄을 섭니다.")
    p1.change_state(ProcessState.READY)
    
    # 3. [실행] 스케줄러가 선택함 (Dispatch)
    print("\n [3. Dispatch] CPU를 할당받았습니다!")
    p1.change_state(ProcessState.RUNNING)
    
    # 4. [작업] CPU가 1초 동안 일을 시킴 (Tick)
    print("\n [4. Execution] 1초간 실행 중...")
    p1.tick() # 남은 시간 3 -> 2
    print(f"   -> 상태: {p1}")
    
    # 5. [중단] I/O 요청 발생 (Blocking)
    print("\n [5. I/O Request] 키보드 입력을 기다립니다.")
    p1.change_state(ProcessState.WAITING)
    
    # 6. [대기] I/O 완료 (Wakeup)
    print("\n [6. I/O Complete] 입력 완료! 다시 줄을 섭니다.")
    # 주의: Waiting -> Running은 불가능! Ready로 가야 함.
    p1.change_state(ProcessState.READY)
    
    # 7. [재실행] 다시 CPU 잡음
    print("\n [7. Dispatch] 다시 CPU를 잡았습니다!")
    p1.change_state(ProcessState.RUNNING)
    
    # 8. [마무리] 남은 2초를 마저 실행
    print("\n [8. Execution] 남은 작업을 수행합니다...")
    p1.tick() # 남은 시간 2 -> 1
    print(f"   -> 1초 실행 후: {p1}")
    
    p1.tick() # 남은 시간 1 -> 0
    print(f"   -> 1초 실행 후: {p1}")
    
    # 9. [종료] 작업 완료
    if p1.remaining_time == 0:
        print("\n [9. Terminated] 모든 작업이 끝났습니다.")
        p1.change_state(ProcessState.TERMINATED)

    print("\n--- [CPU 실행 종료] ---")


if __name__ == "__main__":
    main()
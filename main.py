from process import Process, ProcessState
def main():
    print("---미니 프로세스 시뮬레이터 시작---")

    #모의 시나리오

    # 새로운 프로세스 생성
    p1 = Process(0, 5)

    print("\n--- [정상적인 시나리오 테스트] ---")
    # New -> Ready (가능)
    p1.change_state(ProcessState.READY)

    # Ready -> Running (가능)
    p1.change_state(ProcessState.RUNNING)
    
    # Running -> Waiting (가능: I/O 요청)
    p1.change_state(ProcessState.WAITING)
    
    print("\n--- [비정상적인 시나리오 테스트] ---")

    # Waiting -> Running (불가능. 새치기 금지)
    # 반드시 Waiting -> Ready -> Running 순서여야 함
    print(">> 시도: Waiting에서 바로 Running으로 가보자")
    p1.change_state(ProcessState.RUNNING)
    
    # Waiting -> Ready (가능)
    print("\n>> 시도: Waiting에서 Ready로는 갈 수 있나?")
    p1.change_state(ProcessState.READY) 

    # CPU 실행 종료 메시지 출력
    print("\n--- [CPU 실행 종료] ---")

if __name__ == "__main__":
    main()
from process import Process, ProcessState
def main():
    print("---미니 프로세스 시뮬레이터 시작---")

    #모의 시나리오

    # 1. 새로운 프로세스 생성
    p1 = Process(0, 5)

    # 2. 초기 상태 확인
    print(f"\n1. 생성 직후 상태: {p1.state}")
    
    # 3. 상태 변경 시뮬레이션
    print("\n2. OS가 프로세스를 준비 큐(Ready Queue)로 보냅니다.")
    p1.state = ProcessState.READY
    print(f"   -> 현재 상태: {p1}")  # __repr__ 덕분에 예쁘게 나옴
    
    print("\n3. 스케줄러가 이 프로세스를 선택해서 CPU를 줬습니다!")
    p1.state = ProcessState.RUNNING
    print(f"   -> 현재 상태: {p1}")
    
    print("\n4. 갑자기 키보드 입력을 받아야 해서 대기합니다.")
    p1.state = ProcessState.WAITING
    print(f"   -> 현재 상태: {p1}")

    #4. CPU 실행 종료 메시지 출력
    print("\n--- [CPU 실행 종료] ---")

if __name__ == "__main__":
    main()
from process import Process

def main():
    print("---미니 프로세스 시뮬레이터 시작---")

    #모의 시나리오

    #1. 0초에 도착, 3초동안 실행되는 프로세스 하나 생성
    p1 = Process(arrival_time=0, burst_time=3)

    #2. 생성 직후의 남은 시간 출력
    print(f"\n[초기 상태] 남은 시간: {p1.remaining_time}")


    #3. CPU실행 시뮬레이션
    print("\n--- [CPU 실행 시작] ---")

    #4. 3단위 시간 동안 CPU가 프로세스를 실행
    for i in range(3):
        print(f"⏱️  Tick {i+1}: CPU가 프로세스를 실행합니다...")

        #5. 프로세스의 tick 메서드를 호출하여 1단위 시간 동안 실행 시뮬레이션
        p1.tick() 

        #6. 현재 남은 시간과 프로그램 카운터(PC) 출력
        print(f"   -> [PID {p1.pid}] 남은 시간: {p1.remaining_time}, PC: {p1.registers['PC']}")

    #7. CPU 실행 종료 메시지 출력
    print("\n--- [CPU 실행 종료] ---")

if __name__ == "__main__":
    main()
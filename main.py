from process import Process

def main():
    print("---미니 프로세스 시뮬레이터 시작---")
    
    #모의 시나리오

    #1. 1번 프로세스: 0초에 도착, 3초 동안 실행 
    p1 = Process(arrival_time=0, burst_time=3)

    #2. 2번 프로세스: 1초에 도착, 5초 동안 실행
    p2 = Process(arrival_time=1, burst_time=5)
    
    #3. 3번 프로세스: 2초에 도착, 2초 동안 실행 
    p3 = Process(arrival_time=2, burst_time=2)

    #4. 각 프로세스들의 PID 출력
    print("\n[메모리 확인]")
    print(f"P1의 PID: {p1.pid}")  
    print(f"P2의 PID: {p2.pid}")  
    print(f"P3의 PID: {p3.pid}")  

    print("---미니 프로세스 시뮬레이터 종료---")

if __name__ == "__main__":
    main()
from process import Process

def main():
    print("---미니 프로세스 시뮬레이터 시작---")

    #모의 시나리오

    #1. 프로세스 하나 생성
    p1 = Process(arrival_time=0, burst_time=3)

    #2. 생성 직후의 레지스터 상태 확인
    print(f"\n[PID {p1.pid}의 초기 레지스터 상태]")
    print(p1.registers)


    #3. CPU가 p1을 실행한 후의 레지스터 상태 변경 시뮬레이션
    print("\n--- [시나리오: CPU가 p1을 3초간 실행했다고 가정] ---")

    #4. 가상의 CPU가 p1을 실행해서 PC(프로그램 카운터)가 증가했다고 가정
    p1.registers["PC"] = 3

    #5. AX 레지스터에 어떤 계산 결과 10이 저장되었다고 가정
    p1.registers["AX"] = 10  
    
    print(f"[PID {p1.pid}의 실행 후 레지스터 상태 (Context Save)]")
    print(p1.registers) 

    print("---미니 프로세스 시뮬레이터 종료---")

if __name__ == "__main__":
    main()
class Process:
    _pid_counter = 1  # 클래스 변수로 프로세스 ID를 관리
    def __init__(self, arrival_time, burst_time): #arrvial_time = 프로세스가 도착한 시간, burst_time = 프로세스가 CPU를 점유하는 시간
        
        #1. 프로세스가 생성될 때마다 고유한 프로세스 ID를 부여함
        self.pid = Process._pid_counter

        #2. 다음 프로세스를 위해 프로세스 ID 카운터를 증가시킴
        Process._pid_counter += 1

        #3. 프로세스의 도착 시간과 실행 시간을 설정함
        self.arrival_time = arrival_time
        self.burst_time = burst_time

        #4. 레지스터(context) 초기화. CPU 레지스터를 딕셔너리로 표현.
        # 레지스터란, cpu 내부에 있는 아주 빠른 임시 저장 공간임.
        # cpu는 한 번에 한 프로세스만 실행시킬 수 있으므로, 프로세스들의 상태를 임시로 저장하는데 사용됨.
        self.registers = {
            # 프로그램 카운터, 현재 실행 중인 명령어의 주소를 가리킴. 
            # 쉽게 말해, 이 프로세스의 명령어가 어디까지 실행되었는지를 나타냄.
            'PC' : 0, 

            # 스택 포인터, 스택의 최상단 주소를 가리킴
            # 쉽게 말해, 지금 이 프로세스가 무슨 작업을 하고 있었는지를 나타냄.
            'SP' : 0,

            # 일반 목적 레지스터들, CPU가 데이터를 임시로 저장하는 용도
            # 쉽게 말해, 이 프로세스가 계산을 하거나 데이터를 처리할 때 사용하는 임시 저장 공간임.
            "AX": 0,  
            "BX": 0   

        }

        #5. 남은 실행 시간, 프로세스가 CPU를 얼마동안이나 더 점유해야 하는지를 나타냄
        self.remaining_time = burst_time  

        #6. 대기 시간, 프로세스가 대기 상태에 있었던 총 시간을 나타냄
        self.waiting_time = 0

        #7. 프로세스 생성 메시지를 출력함
        print(f"✨ [PID: {self.pid}] 프로세스 생성!")
        print(f"(도착: {arrival_time}, 실행시간: {burst_time}, 남은시간: {self.remaining_time})")
        print(f"(Context 초기화 완료)")


    #8. 프로세스가 1 단위 시간 동안 실행됨을 시뮬레이션하는 메서드
    def tick(self):
        if self.remaining_time > 0:
            #9. 프로세스가 실행되고 있으므로 남은 시간을 1 단위씩 감소시킴
            self.remaining_time -= 1

            #10. 현재 프로세스가 실행중이므로 프로그램 카운터(PC)를 1 단위씩 증가시킴
            self.registers["PC"] += 1
        else:
            print(f"[PID: {self.pid}] 이미 완료된 프로세스입니다.")
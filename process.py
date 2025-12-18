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
            'SP' : 0,

            # 일반 목적 레지스터들, CPU가 데이터를 임시로 저장하는 용도
            "AX": 0,  
            "BX": 0   

        }

        #5. 프로세스 생성 메시지를 출력함
        print(f"✨ [PID: {self.pid}] 프로세스 생성!")
        print(f"(도착: {arrival_time}, 실행시간: {burst_time})")
        print(f"(Context 초기화 완료)")
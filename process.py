# 파이썬의 내장라이브러리인 enum 모듈에서 Enum 클래스를 가져옴
from enum import Enum

# 1. 프로세스 상태를 정의하는 선택지를 만듬 
class ProcessState(Enum):
    # 2. 프로세스 상태를 나타내는 다양한 상태들을 정의

    #생성
    NEW = "New"     

    #준비            
    READY = "Ready"   

    #실행          
    RUNNING = "Running"         

    #대기
    WAITING = "Waiting"         

    #종료
    TERMINATED = "Terminated"   


# 3. 프로세스 클래스를 정의
class Process:
    # 4. 클래스 변수로 프로세스 ID 카운터를 초기화
    _pid_counter = 1  
    
    # 5. 새로운 프로세스가 만들어지면 호출되는 생성자 메서드, 프로세스의 기본값을 설정함
    # arrival_time: 프로세스가 도착한 시간, burst_time: 프로세스가 실행되는 시간
    def __init__(self, arrival_time, burst_time): 
        
        #6. 프로세스가 생성될 때마다 고유한 프로세스 ID를 부여함
        self.pid = Process._pid_counter

        #7. 다음 프로세스를 위해 프로세스 ID 카운터를 증가시킴
        Process._pid_counter += 1

        #8. 프로세스의 도착 시간과 실행 시간을 설정함
        self.arrival_time = arrival_time
        self.burst_time = burst_time

        #9. 레지스터(context) 초기화. CPU 레지스터를 딕셔너리로 표현.
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

        # 10. PCB에 프로세스의 초기 상태를 NEW로 기록
        self.state = ProcessState.NEW  

        # 남은 실행 시간, 프로세스가 CPU를 얼마동안이나 더 점유해야 하는지를 나타냄
        self.remaining_time = burst_time  

        # 대기 시간, 프로세스가 대기 상태에 있었던 총 시간을 나타냄
        self.waiting_time = 0

        # 프로세스 생성 메시지를 출력함
        print(f"✨ [PID: {self.pid}] 프로세스 생성!")
        print(f"(도착: {arrival_time})")
        print(f"(남은 시간 : {self.remaining_time})")
        print(f"(실행 시간 : {burst_time})")
        print(f"(상태: {self.state.value})")
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
    
    # 프로세스의 상태를 변경하는 메서드, 유효하지 않은 상태 변경은 에러를 발생시킴
    def change_state(self, new_state):
        old_state = self.state
        
        # 같은 상태로 변경하려는 경우 무시
        if old_state == new_state:
            print(f"[PID: {self.pid}] 이미 {new_state.value} 상태입니다.")
            return
        
        # 규칙 위반 검사(허용되지 않는 상태 전환의 경우 막음)
        # [규칙 1] Waiting에서는 오직 Ready로만 갈 수 있음
        if old_state == ProcessState.WAITING and new_state != ProcessState.READY:
            print(f"[PID: {self.pid}] waiting 상태에서는 Ready 상태로만 변경할 수 있습니다.")
            return
        
        # [규칙 2] running으로 변경하려면 반드시 ready 상태여야 함
        if new_state == ProcessState.RUNNING and old_state != ProcessState.READY:
            print(f"[PID: {self.pid}] Running 상태로 변경하려면 Ready 상태여야 합니다.")
            return
        
        # [규칙 3] 종료된 프로세스(Terminated)는 다른 상태로 변경할 수 없음
        if old_state == ProcessState.TERMINATED:
            print(f"[PID: {self.pid}] 종료된 프로세스는 상태를 변경할 수 없습니다.")
            return
        
        # 상태 변경 확정
        self.state = new_state
        print(f"[PID: {self.pid}] 상태 변경: {old_state.value} -> {new_state.value}")

    # 11. 객체인 프로세스를 문자열로 표현하는 매서드로, 개발자가 프로세스의 상태를 쉽게 확인할 수 있도록 함. 
    # 쉽게 말해 프로세스의 정보를 한눈에 보여주는 역할을 함.
    def __repr__(self):
        # 상태는 길이가 재각각이라 보기 싫으므로 보기 좋게 맞춤
        state_str = f"{self.state.name:<10}" 

        # 시간 정보도 보기 좋게 포맷팅
        return (f"[PID:{self.pid:<2} | {state_str} | "
            f"Arrival:{self.arrival_time:>3} | "
            f"Burst:{self.burst_time:>3} | "
            f"Remaining:{self.remaining_time:>3}]")
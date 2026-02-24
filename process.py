from enum import Enum

# 프로세스 상태를 나타내는 Enum 클래스. 각 상태는 프로세스의 생애주기에서 특정 시점을 나타냄
class ProcessState(Enum):
    NEW = "New"     
    READY = "Ready"   
    RUNNING = "Running"         
    WAITING = "Waiting"         
    TERMINATED = "Terminated"   

# 시스템 콜 유형을 나타내는 Enum 클래스. 프로세스가 운영체제에 요청할 수 있는 다양한 시스템 콜을 정의
class SyscallType(Enum):
    NONE = 0
    # I/O 장치(디스크 등) 읽기 요청
    READ_IO = 1   
    # 지정된 시간 동안 대기
    SLEEP = 2    
    # 프로세스 자발적 종료
    EXIT = 3      

# 프로세스 클래스. 각 프로세스는 고유한 PID, 도착 시간, 실행 시간, 우선순위 등을 가짐
class Process:
    # PID 자동 증가를 위한 클래스 변수 
    _pid_counter = 1  
    # 프로세스 생성 시 필요한 정보들을 초기화하는 생성자. arrival_time, burst_time, priority를 인자로 받음
    # (수정 : behavior가 들어올 경우를 대비해 burst_time에 기본값 0을 설정하여 유연성 확보)
    def __init__(self, arrival_time, burst_time=0, priority=0, behavior=None): 
        self.pid = Process._pid_counter
        self.syscall_schedule = []
        Process._pid_counter += 1
        # 프로세스가 시스템에 도착한 시점. 시뮬레이터에서는 이 값을 기반으로 프로세스가 스케줄링 큐에 들어가는 시점을 결정
        self.arrival_time = arrival_time
        # 우선순위는 스케줄링 알고리즘에서 사용될 수 있는 값으로, 기본값은 0 (낮은 우선순위)
        self.priority = priority
        
        # 만약 behavior가 없다면
        if behavior is None:
            # 예전처럼 burst_time만큼 CPU만 쓰는 프로세스로 간주함.
            self.behavior = [("CPU", burst_time)]
            self.burst_time = burst_time
        else:
            self.behavior = behavior
            # 총 실행 시간(burst_time)은 CPU 작업 시간의 합으로 계산
            # Why? I/O 시간은 CPU가 일하는 시간이 아니므로 제외하는 것이 실제 OS 원리에 맞음
            self.burst_time = sum(time for action, time in self.behavior if action == "CPU")
            
        # remaining_time은 프로세스가 CPU에서 실행될 때 남은 실행 시간을 나타내는 변수로, 초기값은 burst_time과 동일하게 설정
        self.remaining_time = self.burst_time

        # 프로세스가 CPU에서 실행될 때 사용할 레지스터를 시뮬레이터에서 간단히 표현하기 위해 딕셔너리 형태로 초기화
        # 레지스터란 CPU 내부에서 데이터를 일시적으로 저장하는 공간
        self.registers = {
            # 프로그램 카운터(PC)는 다음에 실행할 명령어의 주소를 가리키는 레지스터. 시뮬레이터에서는 단순히 명령어 수를 세는 용도로 사용
            'PC' : 0, 
            # 스택 포인터(SP)는 함수 호출 시 스택의 위치를 가리키는 레지스터. 시뮬레이터에서는 사용하지 않지만 초기화는 해둠
            'SP' : 0,
            # AX란, 일반적으로 연산 결과를 저장하는 레지스터. 시뮬레이터에서는 시스템 콜 결과 등을 저장하는 용도로 사용
            "AX": 0, 
            # BX는 보조 레지스터
            "BX": 0   
        }

        self.state = ProcessState.NEW  
        self.waiting_time = 0
        self.turnaround_time = 0 
        self.response_time = -1
        self.first_run_time = -1
        self.syscall_request = None 

        # [페이지 테이블]
        # { VPN : {'pfn': -1, 'valid': False, 'last_access': -1} }
        self.page_table = {} 
        for i in range(4): # 기본 4페이지
            self.page_table[i] = {'pfn': -1, 'valid': False, 'last_access': -1}

    # 프로세스가 한 틱 동안 실행될 때마다 호출되는 메서드로, 프로세스의 행동을 처리하고 시스템 콜 요청을 관리하는 역할을 함
    def tick(self):
        # 더 이상 할 행동이 없으면
        if not self.behavior:
            # 시스템 콜로 EXIT 요청을 예약하여 프로세스가 종료되도록 함. 
            # 이렇게 하면 OS가 다음 틱에 이 프로세스를 TERMINATED 상태로 전환할 수 있음
            self.syscall_request = ("EXIT", 0)
            return

        # 현재 해야 할 행동 확인 (CPU Burst 혹은 I/O Burst의 시작)
        current_action, current_time = self.behavior[0]

        # 만약 현재 해야할 행동이 CPU 연산이라면
        if current_action == "CPU":
            # CPU 연산 수행
            self.remaining_time -= 1
            self.registers["PC"] += 1
            
            # 이 CPU 버스트가 끝났다면 목록에서 제거
            if current_time - 1 == 0:
                self.behavior.pop(0)
                # CPU 버스트가 끝나자마자 다음 행동이 I/O라면 즉시 트랩(Trap) 준비
                if self.behavior and self.behavior[0][0] != "CPU":
                    next_action, next_time = self.behavior[0]
                    self.syscall_request = (next_action, next_time)
                    self.behavior.pop(0) # OS가 접수할 것이므로 미리 제거
            else:
                self.behavior[0] = ("CPU", current_time - 1)
                
        else:
            # CPU 작업이 아니라면 (예: "IO", "SLEEP")
            # How? 현재 행동이 IO라면 직접 실행할 수 없으므로 시스템 콜을 요청함.
            # 이 로직은 CPU가 tick을 호출했을 때 프로세스가 "나 이제 I/O 할래"라고 선언하는 지점임.
            self.syscall_request = (current_action, current_time)
            # 요청했으므로 목록에서는 바로 제거 (OS가 알아서 처리해 줄 거니까)
            self.behavior.pop(0)
    
    def change_state(self, new_state):
        if self.state == new_state:
            return
        self.state = new_state

    # 테스트를 위해 시스템 콜 예약 기능 추가. 특정 실행 시간에 시스템 콜이 발생하도록 예약할 수 있음
    # execute_tick 인자는 프로세스가 CPU에서 실행된 후의 누적 실행 시간을 의미. 
    # 예를 들어, execute_tick이 2라면 프로세스가 CPU에서 2틱 실행된 후에 시스템 콜이 발생
    def add_syscall_schedule(self, execute_tick, sys_type, arg=None):
        self.syscall_schedule.append((execute_tick, sys_type, arg))
        # 실행 시간 순으로 정렬 (먼저 발생할 이벤트가 앞에 오도록)
        self.syscall_schedule.sort(key=lambda x: x[0])

    def check_syscall(self, current_burst_time):
        if not self.syscall_schedule:
            return False
            
        # 예약된 첫 번째 이벤트 확인
        next_event_tick, sys_type, arg = self.syscall_schedule[0]
        
        if current_burst_time == next_event_tick:
            # 시간이 일치하면 시스템 콜 발생
            self.pending_syscall = sys_type
            self.syscall_arg = arg
            
            # 스케줄에서 제거
            self.syscall_schedule.pop(0)
            
            # 로그 출력
            print(f"    [Syscall] PID {self.pid} requests {sys_type.name} (Arg: {arg})")
            return True
            
        return False
        
    def __repr__(self):
        state_str = f"{self.state.name:<10}" 
        return (f"[PID:{self.pid:<2} | {state_str} | "
            f"Prio:{self.priority:>1} | "
            f"AT:{self.arrival_time:>2} | "
            f"BT:{self.burst_time:>2} | "
            f"RT:{self.remaining_time:>2}]")
    
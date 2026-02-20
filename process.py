from enum import Enum

# 프로세스 상태를 나타내는 Enum 클래스. 각 상태는 프로세스의 생애주기에서 특정 시점을 나타냄
class ProcessState(Enum):
    NEW = "New"     
    READY = "Ready"   
    RUNNING = "Running"         
    WAITING = "Waiting"         
    TERMINATED = "Terminated"   

# 프로세스 클래스. 각 프로세스는 고유한 PID, 도착 시간, 실행 시간, 우선순위 등을 가짐
class Process:
    # PID 자동 증가를 위한 클래스 변수 
    _pid_counter = 1  
    # 프로세스 생성 시 필요한 정보들을 초기화하는 생성자. arrival_time, burst_time, priority를 인자로 받음
    def __init__(self, arrival_time, burst_time, priority=0): 
        self.pid = Process._pid_counter
        Process._pid_counter += 1

        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority

        self.registers = {
            'PC' : 0, 
            'SP' : 0,
            "AX": 0,  
            "BX": 0   
        }

        self.state = ProcessState.NEW  
        self.remaining_time = burst_time  
        self.waiting_time = 0
        self.turnaround_time = 0 
        self.response_time = -1
        self.first_run_time = -1

        # [페이지 테이블]
        # { VPN : {'pfn': -1, 'valid': False, 'last_access': -1} }
        self.page_table = {} 
        for i in range(4): # 기본 4페이지
            self.page_table[i] = {'pfn': -1, 'valid': False, 'last_access': -1}

    def tick(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.registers["PC"] += 1
    
    def change_state(self, new_state):
        if self.state == new_state:
            return
        self.state = new_state
        
    def __repr__(self):
        state_str = f"{self.state.name:<10}" 
        return (f"[PID:{self.pid:<2} | {state_str} | "
            f"Prio:{self.priority:>1} | "
            f"AT:{self.arrival_time:>2} | "
            f"BT:{self.burst_time:>2} | "
            f"RT:{self.remaining_time:>2}]")
    
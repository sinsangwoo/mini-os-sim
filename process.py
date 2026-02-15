from enum import Enum

class ProcessState(Enum):
    NEW = "New"     
    READY = "Ready"   
    RUNNING = "Running"         
    WAITING = "Waiting"         
    TERMINATED = "Terminated"   

class Process:
    _pid_counter = 1  
    
    def __init__(self, arrival_time, burst_time, priority=0):
        
        # PID 자동 발급 및 카운터 증가
        self.pid = Process._pid_counter
        Process._pid_counter += 1

        self.arrival_time = arrival_time
        self.burst_time = burst_time

        # 레지스터(Context) 초기화
        self.registers = {
            'PC' : 0, 
            'SP' : 0,
            "AX": 0,  
            "BX": 0   
        }

        # 상태 및 시간 정보 초기화
        self.state = ProcessState.NEW  
        self.remaining_time = burst_time  
        self.waiting_time = 0
        self.turnaround_time = 0 

        # [28일 차 추가] 응답 시간 관련 변수
        self.response_time = -1  # 아직 실행 안 됨을 표시 (-1)
        self.first_run_time = -1 # 처음 CPU 잡은 시간
        self.priority = priority

        # 페이지 테이블 초기화 (가상 주소 -> 물리 주소 매핑)
        self.page_table = {} 
        
        # 예시로 4페이지 할당 (페이지 번호 0~3)
        for i in range(4): # 4페이지 가정
            self.page_table[i] = {'pfn': -1, 'valid': False} 

    def tick(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.registers["PC"] += 1
    
    def change_state(self, new_state):
        old_state = self.state
        
        if old_state == new_state:
            return
        
        # 유효성 검사
        if old_state == ProcessState.WAITING and new_state != ProcessState.READY:
            print(f"[PID:{self.pid}] Error: WAITING -> READY만 가능합니다.")
            return
        
        if new_state == ProcessState.RUNNING and old_state != ProcessState.READY:
            print(f"[PID:{self.pid}] Error: RUNNING은 READY에서만 갈 수 있습니다.")
            return
        
        if old_state == ProcessState.TERMINATED:
            print(f"[PID:{self.pid}] Error: 종료된 프로세스는 변경 불가합니다.")
            return
        
        self.state = new_state
        
        # 상태 변경 로그 (필요시 활성화)
        print(f"[PID: {self.pid}] 상태 변경: {old_state.value} -> {new_state.value}") 
        
    def __repr__(self):
        state_str = f"{self.state.name:<10}" 
        return (f"[PID:{self.pid:<2} | {state_str} | "
            f"Prio:{self.priority:>1} | "
            f"AT:{self.arrival_time:>2} | "
            f"BT:{self.burst_time:>2} | "
            f"RT:{self.remaining_time:>2}]")
    
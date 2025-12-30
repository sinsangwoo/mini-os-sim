class CPU:
    # 프로세스를 실제로 실행하는 하드웨어 유닛
    # 한 번에 하나의 프로세스만 실행할 수 있음
    
    def __init__(self):
        # 현재 CPU를 점유하고 있는 프로세스 (없으면 None)
        self.current_process = None 
        
        # CPU 내부 시계 (총 실행된 틱 수)
        self.time = 0 

    # CPU가 현재 일하고 있는지 확인하는 함수. 
    def is_busy(self):
        # current_process(현재 CPU위에 올려져 있는 프로세스)가 있으면 True, 없으면 False 반환
        return self.current_process is not None

    # 문맥 교환을 수행하는 메서드. 쉽게 말해, CPU 위에 기존의 프로세스를 내리고 새로운 프로세스를 올리는 작업을 하는 함수
    def load_process(self, process):

        # 만약 지금 실행 중인 프로세스가 있다면 쫓아내야 함
        if self.current_process:
            
            # prev_pid 변수가 기존 프로세스의 PID를 저장. 
            prev_pid = self.current_process.pid
            # 원래는 여기서 레지스터 저장 로직이 들어가야 하지만
            # 객체 자체가 PCB이므로 자동으로 저장된 상태라고 생각. 쉽게 말해, self.current_process 객체가 이미 레지스터 값을 가지고 있음
        
        # 만약 현재 실행 중인 프로세스가 없다면 그냥 None 처리. 태
        else:
            prev_pid = "None" 

        # 새로운 프로세스를 CPU에 올림 
        self.current_process = process
        
        # 문맥 교환 로그 출력. 아무것도 못하는 오버헤드 상태가 발생하는 지점
        print(f"[Context Switch] CPU 교체: PID {prev_pid} -> PID {process.pid}")

    
    # CPU를 1 틱 실행하는 메서드
    def run(self):
        # 실행할 프로세스가 없으면 아무것도 안 함 (Idle 상태)
        if not self.current_process:
            return

        # 프로세스에게 1틱동안 실행하라고 지시
        self.current_process.tick()
        
        # CPU 시간도 흐름
        self.time += 1
        
        # 로그 출력 (너무 자주 찍히면 시끄러우니 필요할 때만 주석 해제)
        # print(f" [CPU] PID {self.current_process.pid} 실행 중... (PC: {self.current_process.registers['PC']})")
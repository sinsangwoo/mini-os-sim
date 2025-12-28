class CPU:
    
    def __init__(self):
        # 현재 cpu에서 실행 중인 프로세스
        self.current_process = None 

        # 전체 시간(틱)
        self.time = 0 

    def is_busy(self):
        
        # cpu가 현재 일하고 있는지 확인 
        return self.current_process is not None

    def run(self):
        
        # 현재 프로세스가 있으면 한 틱 실행
        if self.current_process:
            self.current_process.tick()
            # 로그 출력 (선택 사항)
            # print(f"⚙️  CPU Running: PID {self.current_process.pid}")
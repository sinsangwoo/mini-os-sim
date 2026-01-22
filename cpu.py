class CPU:
    # 프로세스를 실제로 실행하는 하드웨어 유닛
    # 한 번에 하나의 프로세스만 실행할 수 있음
    
    def __init__(self):
        # 현재 CPU에 로드된 프로세스
        self.current_process = None 

        # CPU가 동작한 전체 시간 (틱 단위)
        self.time = 0 

        # [25일 차 추가] CPU 버스트 타임 측정을 위한 카운터
        self.cpu_burst_counter = 0
        
        # [26일 차 추가] 문맥 교환 중인지 표시하는 플래그
        self.is_switching = False
        # 문맥 교환에 걸리는 시간 (기본 1틱)
        self.context_switch_time = 1
        # 남은 교체 시간 카운터
        self.switch_counter = 0

    # CPU가 현재 일하고 있는지 확인하는 함수. 
    def is_busy(self):
        # 실행 중이거나, 교체 중이면 바쁜 것임
        return self.current_process is not None or self.is_switching

    # 문맥 교환을 수행하는 메서드. 쉽게 말해, CPU 위에 기존의 프로세스를 내리고 새로운 프로세스를 올리는 작업을 하는 함수
    def load_process(self, process):

        # 만약 지금 실행 중인 프로세스가 있다면 쫓아내야 함
        if self.current_process:
            prev_pid = self.current_process.pid
        else:
            prev_pid = "None"
            
        # [중요] 바로 self.current_process에 할당하지 않고, 임시 변수에 저장하거나
        # 로직을 단순화하기 위해: 
        # 1. 일단 current_process는 None으로 비움 (교체 중엔 아무도 실행 안 함)
        # 2. '다음에 들어올 녀석'을 저장해둠
        self.current_process = None 
        self.next_process_candidate = process # 임시 저장
        
        self.is_switching = True
        self.switch_counter = self.context_switch_time
        
        print(f"   💾 [Switch] Context Change Start: PID {prev_pid} -> PID {process.pid} (Overhead: {self.context_switch_time} tick)")

        # 새로운 프로세스를 CPU에 올림 
        self.current_process = process
        
        # 문맥 교환 로그 출력. 아무것도 못하는 오버헤드 상태가 발생하는 지점
        print(f"   💾 [Switch] Context Change: PID {prev_pid} -> PID {process.pid}")

    
    # CPU를 1 틱 실행하는 메서드
    def run(self):
        # 1. 문맥 교환 중이라면?
        if self.is_switching:
            self.switch_counter -= 1
            if self.switch_counter <= 0:
                # 교체 완료! 드디어 프로세스 탑승
                self.is_switching = False
                self.current_process = self.next_process_candidate
                self.next_process_candidate = None
                self.cpu_burst_counter = 0 # 카운터 초기화
                print(f"   ✅ [Switch] Context Change Complete! PID {self.current_process.pid} is now Running.")
            return # 이번 틱은 교체하느라 썼으니 리턴

        # 2. 실행할 프로세스가 없으면
        if not self.current_process:
            return

        # 3. 정상 실행
        self.current_process.tick()
        self.time += 1
        self.cpu_burst_counter += 1
# io_device.py

# 이 클래스는 I/O 장치의 동작을 시뮬레이션함. 
# 실제 OS에서는 I/O 장치가 데이터를 읽거나 쓰는 작업을 처리하고, 작업이 완료되면 인터럽트를 발생시켜 CPU에 알리는 역할을 하지만 
# 여기서는 간단히 시뮬레이션 형태로 구현.
class IODevice:
    # 장치 이름을 인자로 받아 초기화. 
    # 기본값은 "Disk"로 설정되어 있지만, 필요에 따라 다른 장치 이름으로 생성할 수 있음
    def __init__(self, name="Disk"):
        # 장치 이름 (예: "Disk", "Printer" 등)
        self.name = name
        # I/O 장치 전용 대기 큐: [[process, remaining_time], ...]
        self.wait_queue = [] 
        # I/O 작업이 완료되어 OS가 데려가길 기다리는 프로세스들
        self.finished_queue = [] 

    # I/O 장치가 바쁜지 여부를 반환하는 함수. 대기 큐에 작업이 있으면 바쁘다고 간주
    def is_busy(self):
        return len(self.wait_queue) > 0

    # OS가 프로세스의 I/O 작업을 요청할 때 호출하는 함수. 
    # 프로세스와 필요한 I/O 시간을 인자로 받아 대기 큐에 추가
    def request_io(self, process, time):
        self.wait_queue.append([process, time])
        print(f"    [{self.name}] PID {process.pid} 작업 접수 ({time} 틱)")

    # 매 틱마다 호출되어 I/O 작업을 처리하는 함수. 
    # 대기 큐의 첫 번째 작업을 처리하고, 작업이 완료되면 완료 큐로 이동
    def tick(self):
        if not self.wait_queue:
            return

        # FCFS 방식으로 I/O 처리 (한 번에 하나씩 처리한다고 가정)
        current_req = self.wait_queue[0]
        current_req[1] -= 1 # 남은 시간 1 감소
        
        # 작업이 완료되었는가?
        if current_req[1] <= 0:
            # 작업 완료. 프로세스를 완료 큐로 이동시키고 인터럽트 발생 대기
            process = current_req[0]
            self.wait_queue.pop(0) # 대기 큐에서 제거
            self.finished_queue.append(process) # 완료 큐로 이동
            print(f"    [{self.name}] PID {process.pid} 작업 완료! (인터럽트 발생 대기)")
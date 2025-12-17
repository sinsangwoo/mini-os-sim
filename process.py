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

        #4. 프로세스 생성 메시지를 출력함
        print(f"✨ [PID: {self.pid}] 프로세스 생성! (도착: {arrival_time}, 실행시간: {burst_time})")
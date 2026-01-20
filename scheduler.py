from collections import deque

class Scheduler:
    # 모든 스케줄러의 부모 클래스
    # 공통적으로 사용하는 Ready Queue를 관리
    
    def __init__(self):
        # deque(덱)은 양쪽 끝에서 데이터를 넣고 빼는 속도가 리스트보다 빠름
        # 큐 자료구조로 쓰기에 적합
        self.ready_queue = deque()

    def add_process(self, process):
       # 프로세스를 준비 큐에 추가
        self.ready_queue.append(process)

    def get_next_process(self):
        # 다음에 실행할 프로세스를 결정하여 반환
        raise NotImplementedError("이 메서드는 자식 클래스에서 구현해야 합니다.")
    

# FCFS 스케줄러. First-Come, First-Served 스케줄러라는 뜻으로, 먼저 도착한 프로세스를 먼저 실행하는 비선점형 스케줄러
class FCFS_Scheduler(Scheduler):
    
    # 이 함수의 역할은 준비 큐에서 가장 앞에 있는 프로세스를 꺼내오는 것
    def get_next_process(self):
        if not self.ready_queue:
            return None
        
        return self.ready_queue.popleft()
    

# SJF 스케줄러. Shortest Job First (최단 작업 우선) 스케줄러. 
# Ready Queue에 있는 프로세스 중 burst_time이 가장 작은 것을 선택하는 비선점형 스케줄러
class SJF_Scheduler(Scheduler):
    def get_next_process(self):
        # 큐가 비었으면 None
        if not self.ready_queue:
            return None
        
        # 1. 가장 실행 시간이 짧은 프로세스 찾기
        # min() 함수를 이용해 burst_time이 최소인 객체를 찾습니다.
        shortest_job = min(self.ready_queue, key=lambda p: p.burst_time)
        
        # 2. 큐에서 제거하고 반환
        # deque에서는 remove()가 O(N)이지만, 시뮬레이터 규모에서는 충분히 빠릅니다.
        self.ready_queue.remove(shortest_job)
        
        return shortest_job

# Round Robin 스케줄러. 각 프로세스에 동일한 시간 할당량(time quantum)을 주고 순환하며 실행하는 선점형 스케줄러
class RoundRobin_Scheduler(Scheduler):
    def __init__(self, time_quantum):
        super().__init__() 
        self.time_quantum = time_quantum

    def get_next_process(self):
        if not self.ready_queue:
            return None
        return self.ready_queue.popleft()
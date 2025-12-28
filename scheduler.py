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
        # 자식 클래스(FCFS, RR 등)에서 구체적인 로직을 구현해야 함
        raise NotImplementedError("이 메서드는 자식 클래스에서 구현해야 합니다.")
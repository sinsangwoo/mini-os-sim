from collections import deque

class Scheduler:
    def __init__(self):
        self.ready_queue = deque()

    def add_process(self, process):
        self.ready_queue.append(process)

    def get_next_process(self):
        raise NotImplementedError

class FCFS_Scheduler(Scheduler):
    def get_next_process(self):
        if not self.ready_queue: return None
        return self.ready_queue.popleft()

class SJF_Scheduler(Scheduler):
    def get_next_process(self):
        if not self.ready_queue: return None
        shortest = min(self.ready_queue, key=lambda p: p.burst_time)
        self.ready_queue.remove(shortest)
        return shortest

class RoundRobinScheduler(Scheduler):
    def __init__(self, time_quantum):
        super().__init__()
        self.time_quantum = time_quantum
    
    def get_next_process(self):
        if not self.ready_queue: return None
        return self.ready_queue.popleft()

class PriorityScheduler(Scheduler):
    def get_next_process(self):
        if not self.ready_queue: return None
        highest = min(self.ready_queue, key=lambda p: p.priority)
        self.ready_queue.remove(highest)
        return highest
import time
from process import Process, ProcessState
from scheduler import FCFS_Scheduler, SJF_Scheduler, RoundRobin_Scheduler
from cpu import CPU

def run_simulation(scheduler, job_list, max_time=20):
    # 주어진 스케줄러와 작업 목록으로 시뮬레이션을 수행하고 결과를 반환함
    print(f"\n시뮬레이션 시작 (Scheduler: {type(scheduler).__name__})")
    
    cpu = CPU()
    global_time = 0
    finished_processes = []
    
    # job_list를 복사해서 사용 (원본 보존)
    pending_jobs = list(job_list)
    
    while global_time < max_time:
        print(f"\n[Time: {global_time:>2}] {'='*30}") 

        # 1. [Arrival]
        # 리스트 순회 시 삭제 문제가 발생하지 않도록 복사본이나 인덱스 관리 필요
        # 여기서는 pending_jobs의 복사본을 만들어 순회
        for p in list(pending_jobs): 
            if p.arrival_time == global_time:
                scheduler.add_process(p)
                p.change_state(ProcessState.READY)
                pending_jobs.remove(p)
                print(f"   [Arrival] PID {p.pid} 도착")

        # 2. [Scheduling]
        if not cpu.is_busy():
            next_process = scheduler.get_next_process()
            if next_process:
                cpu.load_process(next_process)
                next_process.change_state(ProcessState.RUNNING)
        
        # 3. [Execution]
        if cpu.is_busy():
            cpu.run()
            current = cpu.current_process
            print(f"    [Run] PID {current.pid} 실행 중 | RT: {current.remaining_time}")
            
            if current.remaining_time == 0:
                print(f"   [Done] PID {current.pid} 종료!")
                current.change_state(ProcessState.TERMINATED)
                current.turnaround_time = (global_time + 1) - current.arrival_time
                finished_processes.append(current)
                cpu.current_process = None 

        # 4. [Aging] 대기 시간 누적
        for p in scheduler.ready_queue:
            p.waiting_time += 1
            
        global_time += 1
        
        # 모든 작업이 완료되었고, 대기 중인 작업도 없으면 조기 종료
        if not pending_jobs and not cpu.is_busy() and not scheduler.ready_queue:
            print("\n모든 작업이 완료되어 시뮬레이션을 조기 종료합니다.")
            break
            
    return finished_processes

def print_report(finished_processes):
    # 시뮬레이션 결과를 표 형태로 출력함
    print("\n" + "="*50)
    print("[Final Report] 시뮬레이션 결과 통계")
    print("="*50)
    print(f"{'PID':<5} | {'Arrival':<8} | {'Burst':<6} | {'Waiting':<8} | {'Turnaround':<10}")
    print("-" * 50)
    
    total_waiting = 0
    total_turnaround = 0
    
    finished_processes.sort(key=lambda x: x.pid)
    
    for p in finished_processes:
        print(f"{p.pid:<5} | {p.arrival_time:<8} | {p.burst_time:<6} | {p.waiting_time:<8} | {p.turnaround_time:<10}")
        total_waiting += p.waiting_time
        total_turnaround += p.turnaround_time
        
    print("-" * 50)
    count = len(finished_processes)
    if count > 0:
        print(f"평균 대기 시간 : {total_waiting / count:.2f}")
        print(f"평균 반환 시간 : {total_turnaround / count:.2f}")
    else:
        print("완료된 프로세스가 없습니다.")
    print("="*50)

def main():
    print("--- 🖥️  Mini OS Simulator: Round Robin Setup ---")
    
    # [시나리오]
    # P1(10초), P2(10초)
    # RR이 작동하면 서로 번갈아가며 실행되어야 함.
    jobs = [
        Process(arrival_time=0, burst_time=10),
        Process(arrival_time=0, burst_time=10)
    ]
    
    # 타임 퀀텀을 2초로 설정
    time_quantum = 2
    rr_scheduler = RoundRobin_Scheduler(time_quantum)
    
    print(f"\n[Experiment] Round Robin (Time Quantum: {time_quantum})")
    print("(아직 선점 로직 미구현으로 FCFS처럼 동작할 것임)")
    
    # 실행
    results = run_simulation(rr_scheduler, jobs, max_time=30)
    print_report(results)

if __name__ == "__main__":
    main()
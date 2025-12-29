from process import Process
from scheduler import FCFS_Scheduler

def main():
    print("--- [11일 차] FCFS 스케줄러 테스트 ---")
    
    # 1. 스케줄러 생성
    scheduler = FCFS_Scheduler()
    print("FCFS 스케줄러 생성 완료")
    
    # 2. 프로세스 3개 생성 (도착 시간 다르게)
    p1 = Process(0, 3)
    p2 = Process(1, 5)
    p3 = Process(2, 2)
    
    # 3. 스케줄러에 순서대로 넣기 
    print("\n[Enqueue] 프로세스를 큐에 넣습니다.")
    scheduler.add_process(p1)
    print(f"   -> P1 추가됨 (현재 큐 크기: {len(scheduler.ready_queue)})")
    
    scheduler.add_process(p2)
    print(f"   -> P2 추가됨 (현재 큐 크기: {len(scheduler.ready_queue)})")
    
    scheduler.add_process(p3)
    print(f"   -> P3 추가됨 (현재 큐 크기: {len(scheduler.ready_queue)})")
    
    # 4. 스케줄러에서 하나씩 꺼내보기 (get_next_process)
    print("\n[Dequeue] 스케줄러에게 다음 프로세스를 요청합니다.")
    
    next_p = scheduler.get_next_process()
    print(f"   -> 첫 번째로 나온 프로세스: PID {next_p.pid} (기대값: 1)")
    
    next_p = scheduler.get_next_process()
    print(f"   -> 두 번째로 나온 프로세스: PID {next_p.pid} (기대값: 2)")
    
    next_p = scheduler.get_next_process()
    print(f"   -> 세 번째로 나온 프로세스: PID {next_p.pid} (기대값: 3)")
    
    # 5. 빈 큐에서 꺼내보기
    next_p = scheduler.get_next_process()
    print(f"   -> 더 꺼낼 게 있는지 확인: {next_p} (기대값: None)")

    print("\n--- 테스트 종료 ---")

if __name__ == "__main__":
    main()
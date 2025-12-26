from process import Process, ProcessState
import random

def main():
    print("--- [CPU 실행 시작] ---\n")

    # 프로세스 공장 생성
    print("\n🏭 [System] 프로세스 5개를 생성하여 Job Queue에 넣습니다.")

    job_queue = []
    for i in range(5):
        # 도착 시간 : i (0에서 4까지 순차적으로 증가)
        # 실행 시간 : 1에서 10 사이의 랜덤 값
        p = Process(arrival_time=i, burst_time=random.randint(1, 10))
        job_queue.append(p)

    # Job Queue 확인. 쉽게 말해, 현재 잡 큐에 있는 프로세스들의 상태를 출력하는 것.
    print(f"\n📋 [Job Queue Status] 총 {len(job_queue)}개의 프로세스 대기 중")
    print("=" * 75) 
    print(f"{'PID':<5} | {'State':<10} | {'Arrival time':<5} | {'Burst time':<5} | {'Remaining time':<5}")
    print("-" * 75)

    for p in job_queue:
        # 객체 내부 데이터를 꺼내서 쓰는 연습. 쉽게 말해, 잡 큐에 있는 프로세스들의 내부 데이터를 출력하는 것.
        print(f"{p.pid:<5} | {p.state.name:<10} | {p.arrival_time:<12} | {p.burst_time:<10} | {p.remaining_time:<12}")

    print("=" * 75)
    # 시나리오 : 모든 프로세스들의 상태를 Ready로 변경하기. 쉽게 말해, OS가 메모리로 프로세스를 로드하는 것.
    # 준비 큐 생성
    ready_queue = []

    # job queue에 있는 모든 프로세스를 꺼내서 준비 큐에 넣기
    while job_queue:
        # pop : 리스트의 맨 앞 요소를 꺼내 반환하고, 리스트에서 제거하는 함수
        p = job_queue.pop(0)

        # 프로세스 상태를 Ready로 변경
        p.change_state(ProcessState.READY)

        # 준비 큐에 추가
        ready_queue.append(p)
    
    # 준비 큐 확인
    print(f"\n📋 [Ready Queue Status] 총 {len(ready_queue)}개의 프로세스 준비 완료")

    # __repr__ 매서드를 활용하여 준비 큐의 상태 출력
    for p in ready_queue:
        print(p)

    print("\n--- [CPU 실행 종료] ---")


if __name__ == "__main__":
    main()
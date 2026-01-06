import time
from process import Process, ProcessState
from scheduler import FCFS_Scheduler
from cpu import CPU

def main():
    print("--- Mini OS Simulator Booting... ---")
    
    scheduler = FCFS_Scheduler()
    cpu = CPU()
    global_time = 0
    
    JOB_LIST = [
        Process(arrival_time=1, burst_time=3),
        Process(arrival_time=3, burst_time=5),
        Process(arrival_time=7, burst_time=2)
    ]
    
    MAX_TIME = 20 # 넉넉하게 늘림
    
    print(f"시스템 초기화 완료. (총 {len(JOB_LIST)}개의 작업 대기 중)\n")
    
    while global_time < MAX_TIME:
        print(f"\n[Time : {global_time}] ------------------------------------")
        
        # [Arrival] 프로세스 도착 (동일)
        # JOB_LIST를 복사본이 아닌 원본으로 순회하면서, 도착한 프로세스를 준비 큐에 추가
        for p in list(JOB_LIST): 

            # 도착 시간이 현재 시간과 같으면 준비 큐에 추가. 
            # 왜 도착 시간과 현재 시간이 같아야 하냐면, 도착 시간이 n인 프로세스는 n틱이 지난 시점에 도착함
            if p.arrival_time == global_time:
                scheduler.add_process(p)

                # Ready 상태로 변경. 
                # Ready 상태란 cpu가 할당되면 바로 실행할 준비가 된 상태
                p.change_state(ProcessState.READY)

                # JOB_LIST에서 제거. 준비 큐에 들어갔으니 더 이상 대기할 필요 없음
                JOB_LIST.remove(p)
                print(f"[Arrival] PID {p.pid} 도착 -> Ready Queue 등록")

        # [Scheduling] CPU가 놀고 있으면 다음 프로세스 할당
        if not cpu.is_busy():
            next_process = scheduler.get_next_process()

            # CPU에 프로세스 로드. 파이썬에서 if문 뒤에 객체만 오는 경우, 객체가 존재하면 아래 명령을 실행하라는 의미
            if next_process:
                cpu.load_process(next_process)
                next_process.change_state(ProcessState.RUNNING)
            else:
                # [수정] 로그가 너무 많아서 IDLE 로그는 생략하거나 간소화
                # print("   (IDLE) 대기 중...") 
                pass

        # [Execution & Termination] 실행 및 종료 처리
        if cpu.is_busy():
            # (1) 일단 1틱 실행
            cpu.run()
            current = cpu.current_process
            print(f"   [Running] PID {current.pid} (남은 시간: {current.remaining_time})")
            
            # (2) [16일 차 추가] 다 끝났는지 검사
            if current.remaining_time == 0:
                print(f"   [Finish] PID {current.pid} 작업 완료")
                
                # 상태 변경 (Running -> Terminated)
                current.change_state(ProcessState.TERMINATED)
                
                # CPU 비우기 (Unload)
                # 다음 루프(Time+1)에서 cpu.is_busy()가 False가 되므로, 
                # 자연스럽게 스케줄러가 다음 프로세스를 가져오게 됨
                cpu.current_process = None 
            
        global_time += 1
        time.sleep(0.5)

    print("\n--- 시뮬레이션 종료 ---")

if __name__ == "__main__":
    main()
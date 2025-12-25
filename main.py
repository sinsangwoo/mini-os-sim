from process import Process, ProcessState
# main.py 예시 구조
def main():
    # 새로운 프로세스 생성
    p1 = Process(0, 5)
    p2 = Process(1, 10)
    p3 = Process(2, 3)

    # 상태를 다양하게 변경
    p1.change_state(ProcessState.RUNNING)
    p2.change_state(ProcessState.READY)

    # 3번 프로세스는 READY -> WAITING으로 상태 변경
    p3.change_state(ProcessState.READY)
    p3.change_state(ProcessState.WAITING)

    # 프로세스 상태 출력
    print("\n--- [프로세스 상태 목록 (Process Table)] ---")

    # 리스트에 담아서 출력해보자
    process_list = [p1, p2, p3]
    
    # 반복문을 돌며 각 프로세스를 출력 (이때 __repr__이 작동함)
    for p in process_list:
        print(p)

    print("\n--- [CPU 실행 종료] ---")


if __name__ == "__main__":
    main()
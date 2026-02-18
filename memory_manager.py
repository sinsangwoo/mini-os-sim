from memory import Memory
from collections import deque



# 메모리 관리자 클래스
class MemoryManager:
    # 생성자
    def __init__(self, memory):
        # 메모리 객체를 받아서 초기화. 메모리 관리자는 메모리를 직접 다루는 역할을 함.
        self.memory = memory
        # 할당된 프레임을 추적하기 위한 FIFO 큐. 페이지 교체 알고리즘에서 사용할 수 있음
        self.fifo_queue = deque()



    # 메모리를 할당하는 메서드. 프로세스가 필요로 하는 페이지 수를 확인하고, 빈 프레임이 충분한지 검사한 후 할당.
    def allocate(self, process):
        required_pages = 4
        allocated_frames = []

        # 4페이지를 확보할 때까지 반복 (빈 자리가 없으면 만들어서라도 채움)
        for i in range(required_pages):
            frame_idx = self.memory.get_free_frame()
            
            #  만약 빈 프레임이 없다면 바로 Swap Out 실행
            if frame_idx == -1:
                frame_idx = self.replace_page() # 여기서 [Swap Out] 로그가 찍힘
            
            # 빈 프레임이었거나, 쫓아내서 만든 프레임에 PID 등록
            if frame_idx != -1:
                self.memory.set_frame(frame_idx, process.pid)
                allocated_frames.append(frame_idx)
            else:
                # 쫓아낼 대상도 없는 정말 심각한 상황 (큐가 비었을 때 등)
                print(f"[Memory Error] OOM! No victim found.")
                return False

        # 4개가 완벽히 모였을 때만 페이지 테이블에 등록 및 FIFO 큐에 추가
        for vpn, pfn in enumerate(allocated_frames):
            process.page_table[vpn] = {'pfn': pfn, 'valid': True}
            self.fifo_queue.append((process, vpn, pfn))
            
        print(f"[Memory] Allocated 4 frames to PID {process.pid}")
        return True



    # FIFO 페이지 교체 알고리즘을 구현한 메서드. 가장 오래된 페이지를 선택하여 쫓아내고, 그 프레임을 반환.

    def replace_page(self):

        if not self.fifo_queue:

            return -1

       

        # 희생자 선정 (맨 앞 녀석)

        victim_process, victim_vpn, victim_pfn = self.fifo_queue.popleft()

       

        # 희생자의 페이지 테이블 업데이트 (Valid=False, PFN=-1)

        # (주의: 프로세스가 이미 종료되었을 수도 있음)

        if victim_vpn in victim_process.page_table:

            victim_process.page_table[victim_vpn]['valid'] = False

            victim_process.page_table[victim_vpn]['pfn'] = -1

            print(f"[Swap Out] PID {victim_process.pid} VPN {victim_vpn} (Frame {victim_pfn}) 쫓겨남!")

           

        # 프레임 비우기 (데이터 삭제는 선택)

        self.memory.free_frame(victim_pfn)

       

        return victim_pfn



    # 메모리 해제 메서드
    def deallocate(self, process):
        for vpn, entry in process.page_table.items():
            # 실제 숫자 데이터인 'pfn'을 꺼냄
            pfn = entry['pfn']
            
            # 할당된 적이 있는 프레임(숫자)인 경우에만 해제 시도
            if pfn != -1:
                self.memory.free_frame(pfn)
        
        # 페이지 테이블 비우기
        process.page_table.clear()
        print(f"[Memory] Deallocated frames for PID {process.pid}")
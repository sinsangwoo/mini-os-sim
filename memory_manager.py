from memory import Memory

# 메모리 관리자 클래스
class MemoryManager:
    # 생성자
    def __init__(self, memory):
        self.memory = memory # 물리 메모리 객체 (하드웨어)

    # 메모리 할당 메서드
    def allocate(self, process):
        # 프로세스가 필요로 하는 페이지 개수 확인
        # (우리는 프로세스마다 크기가 다르다고 가정하고, 일단 burst_time을 크기로 쓰거나 고정 크기로 씀)
        # 여기서는 편의상 '모든 프로세스는 4페이지(16바이트)를 쓴다'고 가정
        required_pages = 4 
        
        # 빈 프레임이 충분한지 확인
        free_frames = []
        for i in range(required_pages):
            frame_idx = self.memory.get_free_frame()
            if frame_idx != -1:
                free_frames.append(frame_idx)
                # 일단 확보해둠 (다른 프로세스가 채가기 전에)
                self.memory.set_frame(frame_idx, process.pid)
            else:
                # [메모리 부족 상황!]
                # 이미 확보한 프레임들도 다시 뱉어내야 함 (Rollback)
                print(f"[Memory Error] Allocation Failed for PID {process.pid} (OOM)")
                for f in free_frames:
                    self.memory.free_frame(f)
                return False
        
        # 페이지 테이블 매핑 (Mapping)
        # { VPN 0 : PFN A, VPN 1 : PFN B ... }
        for vpn, pfn in enumerate(free_frames):
            process.page_table[vpn] = pfn
            
        print(f"[Memory] Allocated {required_pages} frames to PID {process.pid}")
        print(f"   -> Page Table: {process.page_table}")
        return True

    # 메모리 해제 메서드
    def deallocate(self, process):
        for vpn, pfn in process.page_table.items():
            self.memory.free_frame(pfn)
        
        # 페이지 테이블 비우기
        process.page_table.clear()
        print(f"[Memory] Deallocated frames for PID {process.pid}")
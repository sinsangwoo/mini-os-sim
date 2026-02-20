from collections import deque

class MemoryManager:
    def __init__(self, memory):
        self.memory = memory
        # 현재 메모리를 사용 중인 프로세스 목록 (LRU 교체 대상)
        self.active_processes = []

    def allocate(self, process):
        required_pages = 4 
        free_frames = []
        
        # 1. 빈 프레임 확보 시도
        for i in range(required_pages):
            frame_idx = self.memory.get_free_frame()
            if frame_idx != -1:
                free_frames.append(frame_idx)
                self.memory.set_frame(frame_idx, process.pid) # 일단 선점
            else:
                # 2. 부족하면 교체 (LRU)
                victim_frame = self.replace_page_lru()
                if victim_frame != -1:
                    free_frames.append(victim_frame)
                    self.memory.set_frame(victim_frame, process.pid)
                else:
                    # 교체 실패 (OOM) -> 롤백
                    print(f"⚠️ [Memory Error] OOM! Allocation Failed for PID {process.pid}")
                    for f in free_frames:
                        self.memory.free_frame(f)
                    return False
        
        # 3. 매핑
        for vpn, pfn in enumerate(free_frames):
            process.page_table[vpn] = {'pfn': pfn, 'valid': True, 'last_access': 0}
            
        # 관리 목록에 추가 (중복 방지)
        if process not in self.active_processes:
            self.active_processes.append(process)
            
        print(f"[Memory] Allocated {required_pages} frames to PID {process.pid}")
        return True

    def deallocate(self, process):
        for vpn, entry in process.page_table.items():
            if entry['valid']:
                self.memory.free_frame(entry['pfn'])
                entry['valid'] = False
                entry['pfn'] = -1
        
        if process in self.active_processes:
            self.active_processes.remove(process)
            
        print(f"[Memory] Deallocated frames for PID {process.pid}")

    # LRU 페이지 교체 알고리즘 구현. 가장 오래된 접근 시간을 가진 페이지를 찾아서 교체하는 방식
    def replace_page_lru(self):
        victim_process = None
        victim_vpn = -1
        victim_pfn = -1
        min_last_access = float('inf')
        
        found = False
        
        for p in self.active_processes:
            for vpn, entry in p.page_table.items():
                if entry['valid']:
                    if entry['last_access'] < min_last_access:
                        min_last_access = entry['last_access']
                        victim_process = p
                        victim_vpn = vpn
                        victim_pfn = entry['pfn']
                        found = True
        
        if found:
            # 희생자 처단
            victim_process.page_table[victim_vpn]['valid'] = False
            victim_process.page_table[victim_vpn]['pfn'] = -1
            self.memory.free_frame(victim_pfn)
            print(f"[LRU Swap Out] PID {victim_process.pid} VPN {victim_vpn} (Last Access: {min_last_access}) 쫓겨남!")
            return victim_pfn
        
        return -1
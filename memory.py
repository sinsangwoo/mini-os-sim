class Memory:
    PAGE_SIZE = 4 

    def __init__(self, size=1024):
        self.size = size
        self.ram = [0] * size
        self.total_frames = size // Memory.PAGE_SIZE
        self.frames = [None] * self.total_frames
        print(f" [System] Memory Initialized: {size} bytes ({self.total_frames} frames)")

    def read(self, physical_addr):
        if 0 <= physical_addr < self.size:
            return self.ram[physical_addr]
        return None

    def write(self, physical_addr, data):
        if 0 <= physical_addr < self.size:
            self.ram[physical_addr] = data

    def get_free_frame(self):
        for i in range(self.total_frames):
            if self.frames[i] is None:
                return i
        return -1

    def set_frame(self, frame_index, pid):
        if 0 <= frame_index < self.total_frames:
            self.frames[frame_index] = pid
            
    def free_frame(self, frame_index):
        if 0 <= frame_index < self.total_frames:
            self.frames[frame_index] = None
            # 데이터 초기화
            start_addr = frame_index * Memory.PAGE_SIZE
            for i in range(Memory.PAGE_SIZE):
                self.ram[start_addr + i] = 0

    # 메모리 맵을 출력하는 함수. 프레임 번호와 해당 프레임이 어떤 프로세스에 할당되어 있는지 보여줌.
    def print_map(self):
        print("   " + "-" * 40)
        print("     [Physical Memory Map]")
        
        # 한 줄에 8개 프레임씩 출력 (총 128 프레임이므로 16줄)
        frames_per_row = 8
        
        for i in range(0, self.total_frames, frames_per_row):
            row_str = f"   Frame {i:02d}~{min(i+frames_per_row-1, self.total_frames-1):02d}: "
            
            for j in range(frames_per_row):
                idx = i + j
                if idx < self.total_frames:
                    pid = self.frames[idx]
                    if pid is None:
                        row_str += "[  ] " # 빈 프레임
                    else:
                        row_str += f"[P{pid}] " # 사용 중인 프레임
            
            print(row_str)
            
        print("   " + "-" * 40)

class MMU:
    def __init__(self, memory):
        self.memory = memory

    def translate(self, process, virtual_addr, current_time):
        vpn = virtual_addr // Memory.PAGE_SIZE
        offset = virtual_addr % Memory.PAGE_SIZE
        
        if vpn in process.page_table:
            entry = process.page_table[vpn]
            
            if entry['valid']:
                # [LRU] 접근 시간 갱신
                entry['last_access'] = current_time
                
                pfn = entry['pfn']
                physical_addr = (pfn * Memory.PAGE_SIZE) + offset
                return physical_addr
            else:
                return -2 # Page Fault
        else:
            return -1 # Seg Fault
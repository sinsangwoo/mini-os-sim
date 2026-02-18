
# 물리 메모리(RAM)를 시뮬레이션하는 클래스
class Memory:
    # 페이지란 프로세스를 메모리에 적재할 때의 단위임
    # 실제론 페이지 크기는 운영체제마다 다르지만, 여기선 간단히 4바이트로 설정함
    PAGE_SIZE = 4 
    def __init__(self, size=1024):
        # 메모리 크기 설정 (기본 1KB)
        self.size = size
        
        # 실제 저장 공간 (0으로 초기화된 리스트)
        # [0, 0, 0, ... , 0]
        self.ram = [0] * size

        # 총 페이지 수 계산
        self.total_frames = size // Memory.PAGE_SIZE

        # 프레임 테이블 (Frame Table)
        # 각 프레임이 현재 어떤 PID에 의해 사용 중인지 기록 (None이면 빈 프레임)
        # 인덱스 0 = 0~3번지, 인덱스 1 = 4~7번지 ...
        self.frames = [None] * self.total_frames
        
        print(f"[System] Physical Memory Initialized ({size} bytes)")
        print(f"[System] Memory Initialized: {size} bytes ({self.total_frames} frames)")

    # 특정 물리 주소에서 데이터를 읽는 메서드
    def read(self, physical_addr):
        if 0 <= physical_addr < self.size:
            return self.ram[physical_addr]
        else:
            print(f"[Memory Error] 접근 범위 초과 (Read Addr: {physical_addr})")
            return None

    # 특정 물리 주소에 데이터를 쓰는 메서드
    def write(self, physical_addr, data):
        if 0 <= physical_addr < self.size:
            self.ram[physical_addr] = data
            print(f"[Memory] Write {data} -> Addr {physical_addr}")
        else:
            print(f"[Memory Error] 접근 범위 초과 (Write Addr: {physical_addr})")

    # 빈 프레임을 찾는 메서드
    def get_free_frame(self):
        for i in range(self.total_frames):
            if self.frames[i] is None:
                return i
        return -1
    
    # 특정 프레임을 특정 PID에 할당하는 메서드
    def set_frame(self, frame_index, pid):
        if 0 <= frame_index < self.total_frames:
            self.frames[frame_index] = pid
            print(f"[Memory] Frame {frame_index} allocated to PID {pid}")
        else:
            print(f"[Error] Invalid Frame Index: {frame_index}")
            
    # 특정 프레임을 해제하는 메서드
    def free_frame(self, frame_index):
        if 0 <= frame_index < self.total_frames:
            self.frames[frame_index] = None
            # 해당 프레임의 데이터도 0으로 밀어버리는 게 깔끔함 (보안상)
            start_addr = frame_index * Memory.PAGE_SIZE
            for i in range(Memory.PAGE_SIZE):
                self.ram[start_addr + i] = 0
            print(f"[Memory] Frame {frame_index} freed")

    # 메모리 상태를 출력하는 메서드
    def __repr__(self):
        return f"[RAM] Usage: {sum(1 for x in self.ram if x != 0)}/{self.size} bytes used | Head: {self.ram[:20]}..."
    

# 메모리 관리 유닛(MMU) 시뮬레이션 클래스
class MMU:
    def __init__(self, memory):
        self.memory = memory # 물리 메모리 객체 연결

    # 프로세스가 쓰는 가상 주소를 RAM의 물리 주소로 변환하는 메서드
    def translate(self, process, virtual_addr):
        # 가상 주소 분해
        # VPN = VA / Page_Size (몫)
        # Offset = VA % Page_Size (나머지)
        vpn = virtual_addr // Memory.PAGE_SIZE
        offset = virtual_addr % Memory.PAGE_SIZE
        
        # 만약 해당 VPN이 프로세스의 페이지 테이블에 존재한다면
        if vpn in process.page_table:

            # 프로세스의 페이지 테이블에서 해당하는 VPN의 엔트리를 가져옴
            entry = process.page_table[vpn]

            # 만약 페이지가 메모리에 적재되어 있다면 (valid bit가 True)
            if entry['valid']:
                # 실제 물리적 페이지 프레임 번호(PFN)를 가져옴
                pfn = entry['pfn']
                # 물리 주소 = (PFN * 페이지 크기) + 오프셋
                physical_addr = (pfn * Memory.PAGE_SIZE) + offset
                # 주소 변환 해주고
                return physical_addr
            else:
                # 페이지는 존재하지만 메모리에 없음 (Page Fault)
                print(f"[MMU] Page Fault! (VA {virtual_addr}, VPN {vpn} is Invalid)")
                return -2 # Fault 코드
        else:
            # 아예 없는 페이지 (Segmentation Fault)
            print(f"[MMU] Seg Fault! (VA {virtual_addr}, VPN {vpn} Out of Range)")
            return -1 # Error 코드
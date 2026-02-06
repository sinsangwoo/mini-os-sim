
# 물리 메모리(RAM)를 시뮬레이션하는 클래스
class Memory:
    def __init__(self, size=1024):
        # 1. 메모리 크기 설정 (기본 1KB)
        self.size = size
        
        # 2. 실제 저장 공간 (0으로 초기화된 리스트)
        # [0, 0, 0, ... , 0]
        self.ram = [0] * size
        
        print(f"[System] Physical Memory Initialized ({size} bytes)")

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

    # 메모리 상태를 출력하는 메서드
    def __repr__(self):
        return f"[RAM] Usage: {sum(1 for x in self.ram if x != 0)}/{self.size} bytes used | Head: {self.ram[:20]}..."
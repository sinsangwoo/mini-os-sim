# cpu.py
import random

# 이 클래스는 CPU의 동작을 시뮬레이션 함. 
# 실제 OS에서는 CPU가 프로세스를 실행하고, 문맥 교환을 처리하며, 메모리 접근을 수행하는 역할을 하지만 여기서는 간단히 시뮬레이션 형태로 구현.
class CPU:
    # CPU는 MMU를 통해 메모리 접근을 시뮬레이션하기 위해 MMU 객체를 참조함. 
    def __init__(self, mmu):
        # MMU 객체 참조 (메모리 접근 시 필요)
        self.mmu = mmu
        # 현재 CPU에서 실행 중인 프로세스 (없으면 None)
        self.current_process = None 
        # CPU 내부 시간 (프로세스 실행 시 증가)
        self.time = 0 
        # CPU 버스트 카운터 (프로세스가 CPU에서 얼마나 오래 실행되었는지 추적)
        self.cpu_burst_counter = 0
        # 문맥 교환 상태 플래그 (True면 현재 문맥 교환 중)
        self.is_switching = False
        # 문맥 교환에 걸리는 시간 (예: 1 단위 시간)
        self.context_switch_time = 1
        # 문맥 교환 카운터. 문맥 교환이 시작된 후 얼마나 시간이 지났는지 추적
        self.switch_counter = 0
        # 문맥 교환이 완료된 후 다음에 실행할 프로세스 후보. 문맥 교환이 끝나면 이 프로세스를 실행
        self.next_process_candidate = None
        # 페이지 폴트 발생 여부를 알리는 깃발. True면 현재 프로세스가 페이지 폴트 상태
        self.page_fault_flag = False 

    def is_busy(self):
        return self.current_process is not None or self.is_switching

    def load_process(self, process):
        if self.current_process:
            prev_pid = self.current_process.pid
        else:
            prev_pid = "None"
            
        self.current_process = None 
        self.next_process_candidate = process 
        self.is_switching = True
        self.switch_counter = self.context_switch_time
        
        print(f"   [Switch] Context Change Start: PID {prev_pid} -> PID {process.pid}")

    # 
    def run(self):
        # 페이지 폴트 상태에서 실행 시도 시, 문맥 교환으로 간주하여 CPU를 잠시 멈추고 다음 프로세스 후보로 현재 프로세스를 설정
        self.page_fault_flag = False
        # 교환 중이라면
        if self.is_switching:
            # 문맥 교환 중이면 카운터 감소. 
            self.switch_counter -= 1
            # 문맥 교환이 완료되었는지 확인. 문맥 교환이 완료되면 다음 프로세스를 CPU에서 실행할 준비가 됨
            if self.switch_counter <= 0:
                # 문맥 교환 완료. CPU는 이제 다음 프로세스 후보를 실행할 준비가 됨
                self.is_switching = False
                # 현재 실행할 프로세스는 문맥 교환이 완료된 후 실행할 프로세스 후보로 설정. 
                # 문맥 교환이 끝나면 이 프로세스를 CPU에서 실행
                self.current_process = self.next_process_candidate
                # 다음 프로세스 후보 초기화. 문맥 교환 완료 후 실행할 프로세스는 이제 없음
                self.next_process_candidate = None
                # CPU 버스트 카운터 초기화 (새 프로세스 실행 시작)
                self.cpu_burst_counter = 0
                
                # [응답 시간 기록]
                if self.current_process.first_run_time == -1:
                    self.current_process.first_run_time = self.time # 현재 CPU 시간 기준 (또는 global_time 받아와야 함)
                    # 여기서는 편의상 CPU 시간으로 기록 (정확하진 않지만 흐름 파악용)
                    # 정확히 하려면 run() 인자로 global_time을 받아야 함.
                
                print(f"   [Switch] Complete! PID {self.current_process.pid} Running.")
            return

        # 현재 실행 중인 프로세스가 없으면 실행할 프로세스가 없는 상태이므로 그냥 반환
        if not self.current_process:
            return
        
        # [메모리 접근 시뮬레이션]
        if random.random() < 0.3:
            va = random.randint(0, 15)
            if random.choice(["LOAD", "STORE"]) == "LOAD":
                self.load_instruction(va)
            else:
                self.store_instruction(va, random.randint(1, 100))
        
        # 만약 페이지 폴트가 발생했다면, 이번 틱은 무효화 하고 바로 리턴
        if self.page_fault_flag:
            return
        
        # 성공한 경우에만 프로세스 실행. 페이지 폴트가 발생하면 run()이 반환되어 CPU가 문맥 교환 상태로 전환됨
        self.current_process.tick()
        self.time += 1
        self.cpu_burst_counter += 1

    def load_instruction(self, va):
        pa = self.mmu.translate(self.current_process, va, self.time)
        if pa >= 0:
            data = self.mmu.memory.read(pa)
            print(f"      [Mem] LOAD VA:{va} -> PA:{pa} (Data: {data})")
        elif pa == -2:
            print(f"      [Fault] Page Fault! (VA:{va})")
            self.page_fault_flag = True

    def store_instruction(self, va, data):
        pa = self.mmu.translate(self.current_process, va, self.time)
        if pa >= 0:
            self.mmu.memory.write(pa, data)
            print(f"      [Mem] STORE VA:{va} -> PA:{pa} (Data: {data})")
        elif pa == -2:
            print(f"      [Fault] Page Fault! (VA:{va})")
            self.page_fault_flag = True
# cpu.py
import random

# 이 클래스는 CPU의 동작을 시뮬레이션 함. 
# 실제 OS에서는 CPU가 프로세스를 실행하고, 문맥 교환을 처리하며, 메모리 접근을 수행하는 역할을 하지만 여기서는 간단히 시뮬레이션 형태로 구현.
class CPU:
    def __init__(self, mmu):
        self.mmu = mmu
        self.current_process = None 
        self.time = 0 
        self.cpu_burst_counter = 0
        self.is_switching = False
        self.context_switch_time = 1
        self.switch_counter = 0
        self.next_process_candidate = None

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

    def run(self):
        if self.is_switching:
            self.switch_counter -= 1
            if self.switch_counter <= 0:
                self.is_switching = False
                self.current_process = self.next_process_candidate
                self.next_process_candidate = None
                self.cpu_burst_counter = 0
                
                # [응답 시간 기록]
                if self.current_process.first_run_time == -1:
                    self.current_process.first_run_time = self.time # 현재 CPU 시간 기준 (또는 global_time 받아와야 함)
                    # 여기서는 편의상 CPU 시간으로 기록 (정확하진 않지만 흐름 파악용)
                    # 정확히 하려면 run() 인자로 global_time을 받아야 함.
                
                print(f"   [Switch] Complete! PID {self.current_process.pid} Running.")
            return

        if not self.current_process:
            return

        self.current_process.tick()
        self.time += 1
        self.cpu_burst_counter += 1
        
        # [메모리 접근 시뮬레이션]
        if random.random() < 0.3:
            va = random.randint(0, 15)
            if random.choice(["LOAD", "STORE"]) == "LOAD":
                self.load_instruction(va)
            else:
                self.store_instruction(va, random.randint(1, 100))

    def load_instruction(self, va):
        pa = self.mmu.translate(self.current_process, va, self.time)
        if pa >= 0:
            data = self.mmu.memory.read(pa)
            print(f"      [Mem] LOAD VA:{va} -> PA:{pa} (Data: {data})")
        elif pa == -2:
            print(f"      [Fault] Page Fault! (VA:{va})")

    def store_instruction(self, va, data):
        pa = self.mmu.translate(self.current_process, va, self.time)
        if pa >= 0:
            self.mmu.memory.write(pa, data)
            print(f"      [Mem] STORE VA:{va} -> PA:{pa} (Data: {data})")
        elif pa == -2:
            print(f"      [Fault] Page Fault! (VA:{va})")
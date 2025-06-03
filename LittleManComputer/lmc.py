#
# Alice Macuz 
# SM3201385
#

from copy import copy

class LMC:

    class LMCError(Exception):
        pass

    class MemoryLimitError(LMCError):
        pass

    class InputQueueEmptyError(LMCError):
        pass
    
    class InvalidInstructionError(LMCError):
        pass

    def __init__(self, input_values=None):
        self.ram = [0] * 100                  
        self.acc = 0                          # Accumulator
        self.pc = 0                           # Program counter
        self.input_buffer = input_values or []
        self.output_buffer = []
        self.flag = 0  # 1 if over/underflow, 0 otherwise

    def load_program(self, memory_image):
        #
        # carica codice macchina in memoria
        #
        if len(memory_image) > 100:
            raise self.MemoryLimitError("Errore: Programma troppo grande per memoria.")
        self.ram = copy(memory_image)

        def execute(self, mode="n"):
        #
        # esegue tutto il programma oppure step-by-stepp
        #
        try:
            while True:
                self.execute_step(mode)
        except StopIteration:
            print("Esecuzione terminata.")

    def execute_step(self, mode="n"):
        #
        # esegue istruzione dal program counter
        #
        if not (0 <= self.pc < 100):
            raise self.MemoryLimitError("Errore: Accesso memoria invalido.")

        instruction = self.ram[self.pc]
        opcode = instruction // 100
        address = instruction % 100
        self._decode_and_run(opcode, address)

        if mode.lower() == "s":
            self._display_debug()
            input("Premere INVIO per continuare...")
    
    def _decode_and_run(self, opcode, address):
        #
        # decodifica ed esegue un'istruzione
        #
        if opcode == 1:  # ADD
            result = self.acc + self.ram[address]
            self.acc = result % 1000
            self.flag = 1 if result > 999 else 0
            self.pc += 1

        elif opcode == 2:  # SUB
            result = self.acc - self.ram[address]
            self.acc = result % 1000
            self.flag = 1 if result < 0 else 0
            self.pc += 1

        elif opcode == 3:  # STA
            self.ram[address] = self.acc
            self.pc += 1

        elif opcode == 5:  # LDA
            self.acc = self.ram[address]
            self.pc += 1

        elif opcode == 6:  # BRA (unconditional)
            self.pc = address

        elif opcode == 7:  # BRZ (branch if zero)
            if self.acc == 0 and self.flag == 0:
                self.pc = address
            else:
                self.pc += 1

        elif opcode == 8:  # BRP (branch if positive)
            if self.flag == 0:
                self.pc = address
            else:
                self.pc += 1

        elif opcode == 9:
            if address == 1:  # INP
                if not self.input_buffer:
                    raise self.InputQueueEmptyError("Errore: Input buffer vuoto.")
                self.acc = self.input_buffer.pop(0)
                self.pc += 1
            elif address == 2:  # OUT
                self.output_buffer.append(self.acc)
                self.pc += 1
            else:
                raise self.InvalidInstructionError(f"Errore: I/O opcode sconosciuto: 9{address}")

        elif opcode == 0:  # HLT
            raise StopIteration

        else:
            raise self.InvalidInstructionError(f"Errore: Istruzione non ammessa: {opcode}{address}")
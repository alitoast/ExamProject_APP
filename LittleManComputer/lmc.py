#
# Alice Macuz 
# SM3201385
#

from copy import copy

class LMC:

    class MemoryLimitError(LMCError):
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
    
    
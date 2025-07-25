#
# Alice Macuz 
# SM3201385
#

"""
lmc.py — Simulatore della macchina Little Man Computer (LMC).
Emula l'esecuzione di istruzioni LMC con memoria, accumulatore e gestione I/O.
"""


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
        self.ram = [0] * 100                  # Memoria 100 celle
        self.acc = 0                          # Accumulatore
        self.pc = 0                           # Program counter
        self.input_buffer = input_values or []# Coda input
        self.output_buffer = []               # Coda output
        self.flag = 0  # 1 if over/underflow, 0 altrimenti

    def load_program(self, memory_image):
        """
        Carica un programma in memoria.
        """
        if len(memory_image) > 100:
            raise self.MemoryLimitError("Errore: Programma troppo grande per memoria.")

        self.ram = copy(memory_image)

    def execute(self, mode="n"):
        """
        Esegue il programma caricato:
        - 'c' o qualsiasi altro valore: esecuzione continua
        - 's': esecuzione passo-passo con debug
        """
        try:
            while True:
                self.execute_step(mode)
        except StopIteration:
            print("Esecuzione terminata.")

    def execute_step(self, mode="n"):
        """
        Esegue una singola istruzione dal program counter.
        Se in modalità step-by-step, mostra lo stato della memoria dopo l'esecuzione.
        """
        if not (0 <= self.pc < 100):
            raise self.MemoryLimitError("Errore: Accesso memoria invalido.")

        # recupera l'istruzione corrente dalla memoria
        instruction = self.ram[self.pc]

        # decodifica l'istruzione: le prime 1-2 cifre sono l'opcode, le ultime due l'indirizzo
        opcode = instruction // 100
        address = instruction % 100

        # esegue l'istruzione decodificata
        self._decode_and_run(opcode, address)

        # se la modalità è step-by-step, mostra lo stato interno e attende input
        if mode.lower() == "s":
            self._display_debug()
            input("Premere INVIO per continuare.")
    
    def _decode_and_run(self, opcode, address):
        """
        Decodifica l'opcode e delega l'esecuzione alla funzione corrispondente.
        """
        if opcode == 1:  # ADD
            self._handle_add(address)
        elif opcode == 2:  # SUB
            self._handle_sub(address)
        elif opcode == 3:  # STA
            self._handle_sta(address)
        elif opcode == 5:  # LDA
            self._handle_lda(address)
        elif opcode == 6:  # BRA (unconditional)
            self._handle_bra(address)
        elif opcode == 7:  # BRZ (branch if zero)
            self._handle_brz(address)
        elif opcode == 8:  # BRP (branch if positive)
            self._handle_brp(address)
        elif opcode == 9:  # I/O
            self._handle_io(address)
        elif opcode == 0:  # HLT
            self._handle_hlt()
        else:
            raise self.InvalidInstructionError(f"Errore: Istruzione non ammessa: {opcode}{address}")

    # Handler istruzioni

    def _handle_add(self, address):
        self._check_address(address)
        result = self.acc + self.ram[address]
        self.flag = 1 if result > 999 else 0  # flag = 1 se overflow
        self.acc = result % 1000              # simula registri a 3 cifre (max 999)
        self.pc += 1                          # passa all'istruzione successiva


    def _handle_sub(self, address):
        self._check_address(address)
        result = self.acc - self.ram[address]
        self.flag = 1 if result < 0 else 0    # flag = 1 se underflow
        self.acc = result % 1000
        self.pc += 1

    def _handle_sta(self, address):
        self._check_address(address)
        self.ram[address] = self.acc
        self.pc += 1

    def _handle_lda(self, address):
        self._check_address(address)
        self.acc = self.ram[address]
        self.pc += 1

    def _handle_bra(self, address):
        self._check_address(address)
        self.pc = address

    def _handle_brz(self, address):
        self._check_address(address)
    
        if self.acc == 0 and self.flag == 0:
            self.pc = address
        else:
            self.pc += 1

    def _handle_brp(self, address):
        self._check_address(address)

        if self.flag == 0:
            self.pc = address
        else:
            self.pc += 1

    def _handle_io(self, address):
        """
        Gestisce le operazioni di input/output:
        - INP (901): legge un valore dal buffer di input nell'accumulatore
        - OUT (902): scrive il contenuto dell'accumulatore nel buffer di output
        """
        self._check_address(address)

        if address == 1:  # INPUT
            if not self.input_buffer:
                raise self.InputQueueEmptyError("Errore: Input buffer vuoto impossibile eseguire istruzione.")

            value = self.input_buffer.pop(0) # preleva e rimuove il primo valore in input

            # validazione del valore ricevuto
            if value < 0 or value > 999:
                raise ValueError(f"Valore di input non valido: {value}")

            self.acc = value

        elif address == 2:  # OUTPUT
            self.output_buffer.append(self.acc) # scrive l'accumulatore nell'output
            
        else:
           raise self.InvalidInstructionError(f"Errore: opcode I/O sconosciuto: 9{address}")
        self.pc += 1

    def _handle_hlt(self):
        raise StopIteration

    def get_output(self):
        return self.output_buffer

    def _display_debug(self):
        """
        Mostra lo stato interno della macchina durante l'esecuzione passo-passo.
        """
        print(f"\nPC: {self.pc} | ACC: {self.acc} | FLAG: {self.flag}")
        print("Memoria:")

        for i in range(0, 100, 10):
            row = ' '.join(f"{cell:03}" for cell in self.ram[i:i+10])
            print(f"{i:02}-{i+9:02}: {row}")

        print(f"Input buffer: {self.input_buffer}")
        print(f"Output buffer: {self.output_buffer}")

    def _check_address(self, address):
        if not 0 <= address < 100:
            raise self.MemoryLimitError(f"Errore: Indirizzo memoria non valido: {address}")

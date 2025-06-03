#
# Alice Macuz 
# SM3201385
#

class Assembler:
    def __init__(self):
        self.opcodes ={
            "ADD": 1, "SUB": 2, "STA": 3, "LDA": 5,
            "BRA": 6, "BRZ": 7, "BRP": 8,
            "INP": 901, "OUT": 902, "HLT": 0,
            "DAT": None}
        self.labels = {}
        self.memory = [0] * 100
    
    def assemble(self, source_code:str):
        source_lines = self._clean_source(source_code)
        self._resolve_labels(source_lines)
        self._to_machine_code(source_lines)
        return self.memory
    
    def _clean_source(self, source_code: str):
        #
        # pulisce source_code da commenti e linee vuote
        #
        source_lines = source_code.splitlines()
        cleaned = []
        for line in source_lines:
            line = line.split("//")[0].strip()
            if line:
                cleaned.append(line)
        return cleaned
    
    def _resolve_labels(self, source_lines):
        #
        # mappa labels to indirizzi memoria
        #
        current_address = 0

        for line in source_lines:
            parts = line.split(maxsplit=1)

            # se la prima parola non è un'istruzione, allora è una label
            if len(parts) > 1 and parts[0].upper() not in self.opcodes:
                label = parts[0].upper()

                if label in self.label_table:
                    raise ValueError("Errore: Label duplicata")

                self.label_table[label] = current_address

            # conta line come istruzione e avanza l'indirizzo mem
            if len(parts) > 1 or parts[0].upper() in self.opcodes:
                current_address += 1

            # controlla bounds
            if current_address > 100:
                raise MemoryError("Errore: Il programma eccede la memoria dell'LMC (100 celle).")

    def _to_machine_code(self, source_lines):
        #
        # converte istruzioni in codice macchina
        #
        current = 0

        for line in source_lines:
            parts = line.split(maxsplit=2)

            # rimuove label se presente
            if len(parts) > 1 and parts[0].upper() not in self.opcodes:
                parts.pop(0)

            instr = parts[0].upper()
            operand = parts[1] if len(parts) > 1 else None

            if instr not in self.opcodes:
                raise ValueError("Errore: istruzione invalida.")

            # gestione DAT
            if instr == "DAT":
                value = int(operand) if operand else 0
                self.memory[current] = value

            # gestione INP, OUT, HLT
            elif instr in ("INP", "OUT", "HLT"):
                self.memory[current] = self.opcodes[instr]

            # tutte le altre, che richiedono indirizzo
            else:
                if operand is None:
                    raise ValueError("Errore: operando mancante.")

                # conversione a numerico
                if operand.isdigit():
                    address = int(operand)
                elif operand.upper() in self.label_table:
                    address = self.label_table[operand.upper()]
                else:
                    raise ValueError("Errore: Label non definita")

                # combina opcode e address (es, ADD 03 → 103)
                self.memory[current] = self.opcodes[instr] * 100 + address

            current += 1
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
        try:
            source_lines = self._clean_source(source_code)
            self._resolve_labels(source_lines)
            self._to_machine_code(source_lines)
            return self.memory
        except Exception as e:
            raise RuntimeError(f"Errore: assemblaggio fallito: {str(e)}.")
    
    def _clean_source(self, source_code: str):
        """
        pulisce source_code da commenti e linee vuote
        """
        source_lines = source_code.splitlines()
        cleaned = []
        for line in source_lines:
            line = line.split("//")[0].strip()
            if line:
                cleaned.append(line)
        return cleaned
    
    def _resolve_labels(self, source_lines):
        """
        mappa labels to indirizzi memoria
        """
        current_address = 0

        for line in source_lines:
            parts = line.split(maxsplit=1)

            # se la prima parola non è un'istruzione, allora è una label
            if len(parts) > 1 and parts[0].upper() not in self.opcodes:
                label = parts[0].upper()

                if label in self.labels:
                    raise ValueError(f"Errore: Label duplicata: {label}.")

                self.labels[label] = current_address

            # conta line come istruzione e avanza l'indirizzo di memoria
            if len(parts) > 1 or parts[0].upper() in self.opcodes:
                current_address += 1

            # controlla bounds
            if current_address > 100:
                raise MemoryError("Errore: Il programma eccede la memoria dell'LMC (100 celle).")

    def _to_machine_code(self, source_lines):
        """
        converte istruzioni in codice macchina
        """
        current_address = 0
        for line in source_lines:
            instr, operand = self._parse_instruction(line)

            if instr not in self.opcodes:
                raise ValueError(f"Errore: Istruzione non valida: {instr}.")

            if instr == "DAT":
                self.memory[current_address] = self._resolve_dat(operand)
            elif instr in ("INP", "OUT", "HLT"):
                if operand is not None:
                    raise ValueError(f"Errore: L'istruzione {instr} non accetta operandi.")
                self.memory[current_address] = self.opcodes[instr]
            else:
                self.memory[current_address] = self._resolve_instruction_with_operand(instr, operand)

            current_address += 1

    def _parse_instruction(self, line):
        """
        estrae istruzione e operando, rimuove label se presente
        """
        parts = line.split(maxsplit=2)
        if len(parts) > 1 and parts[0].upper() not in self.opcodes:
            parts.pop(0)  # rimuove label
        instr = parts[0].upper()
        operand = parts[1] if len(parts) > 1 else None
        return instr, operand
        
    def _resolve_dat(self, operand):
        """
        risolve il valore di una direttiva DAT
        """
        if operand is None:
            return 0
        if operand.isdigit():
            return int(operand)
        elif operand.upper() in self.labels:
            return self.labels[operand.upper()]
        else:
            raise ValueError(f"Errore: Label non definita in DAT: {operand}.")

    def _resolve_instruction_with_operand(self, instr, operand):
        """
        risolve istruzioni con operando (es. ADD, STA)
        """
        if operand is None:
            raise ValueError(f"Errore: Operando mancante per istruzione: {operand}.")
        if operand.isdigit():
            address = int(operand)
        elif operand.upper() in self.labels:
            address = self.labels[operand.upper()]
        else:
            raise ValueError(f"Errore: Label non definita: {operand}.")
        
        # validazione range operando
        if address < 0 or address >= 100:
            raise ValueError(f"Errore: Operando fuori range per {instr}: {address}.")

        return self.opcodes[instr] * 100 + address
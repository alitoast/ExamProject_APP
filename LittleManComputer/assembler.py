#
# Alice Macuz 
# SM3201385
#

"""
assembler.py — Assembler per il simulatore Little Man Computer (LMC).
Traduce codice assembly .lmc in codice macchina.
"""


class Assembler:
    def __init__(self):
        # dizionario che associa le istruzioni LMC al loro opcode
        self.opcodes ={
            "ADD": 1, "SUB": 2, "STA": 3, "LDA": 5,
            "BRA": 6, "BRZ": 7, "BRP": 8,
            "INP": 901, "OUT": 902, "HLT": 0,
            "DAT": None
        }
        self.labels = {}
        self.memory = [0] * 100
    
    def assemble(self, source_code: str):
        """
        Funzione principale dell'Assembler:
        - Prima passata: risolve le etichette.
        - Seconda passata: converte le istruzioni in codice macchina.
        Restituisce la memoria LMC pronta per l'esecuzione
        """
        try:
            source_lines = self._clean_source(source_code)
            self._resolve_labels(source_lines)
            self._to_machine_code(source_lines)
            return self.memory

        except Exception as e:
            raise RuntimeError(f"Errore: assemblaggio fallito: {str(e)}.")
    
    def _clean_source(self, source_code: str):
        """
        Elimina i commenti (dopo //) e le righe vuote dal sorgente.
        Ritorna una lista di righe pulite.
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
        Prima passata: associa ogni label al suo indirizzo in memoria.
        """
        current_address = 0

        for line in source_lines:
            elements = line.split(maxsplit=1)

            # se la prima parola non è un'istruzione, allora è una label
            if len(elements) > 1 and elements[0].upper() not in self.opcodes:
                label = elements[0].upper()

                if label in self.labels:
                    raise ValueError(f"Errore: Label duplicata: {label}.")

                self.labels[label] = current_address

            # conta ogni riga come istruzione (con o senza label)
            if len(elements) > 1 or elements[0].upper() in self.opcodes:
                current_address += 1

            # controlla che non si superi la memoria LMC
            if current_address > 100:
                raise MemoryError("Errore: Il programma eccede la memoria dell'LMC (100 celle).")

    def _to_machine_code(self, source_lines):
        """
        Seconda passata: converte ogni istruzione in formato numerico (codice macchina)
        e la salva nella memoria simulata.
        """
        current_address = 0
        for line in source_lines:
            # estrae l'istruzione e l'eventuale operando dalla riga
            instr, operand = self._parse_instruction(line)
            
            # verifica che l'istruzione sia valida
            if instr not in self.opcodes:
                raise ValueError(f"Errore: Istruzione non valida: {instr}.")

            if instr == "DAT":
                self.memory[current_address] = self._resolve_dat(operand)
            elif instr in ("INP", "OUT", "HLT"):
                # queste istruzioni non accettano operandi
                if operand is not None:
                    raise ValueError(f"Errore: L'istruzione {instr} non accetta operandi.")
                self.memory[current_address] = self.opcodes[instr]
            else:
                # per le istruzioni con operando (ADD, STA, etc.)
                self.memory[current_address] = self._resolve_instruction_with_operand(instr, operand)

            current_address += 1

    def _parse_instruction(self, line):
        """
        Estrae istruzione e operando da una riga.
        Rimuove l'etichetta iniziale se presente.
        Ritorna una tupla (istruzione, operando).
        """
        elements = line.split(maxsplit=2)
        if len(elements) > 1 and elements[0].upper() not in self.opcodes:
            elements.pop(0)  # rimuove label

        instr = elements[0].upper()
        operand = elements[1] if len(elements) > 1 else None
        return instr, operand
        
    def _resolve_dat(self, operand):
        """
        Gestisce la direttiva DAT, che riserva spazio in memoria.
        Può contenere un valore numerico iniziale o un riferimento a una label.
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
        Converte istruzioni che richiedono un operando (es. ADD, STA, LDA)
        in codice macchina (opcode * 100 + indirizzo).
        Ritorna un int che rappresenta l'istruzione in codice machcchina.
        """
        if operand is None:
            raise ValueError(f"Errore: Operando mancante per istruzione: {operand}.")

        # risolve indirizzo numerico diretto o label
        if operand.isdigit():
            address = int(operand)
        elif operand.upper() in self.labels:
            address = self.labels[operand.upper()]
        else:
            raise ValueError(f"Errore: Label non definita: {operand}.")
        
        # controllo che l'indirizzo sia valido
        if address < 0 or address >= 100:
            raise ValueError(f"Errore: Operando fuori range per {instr}: {address}.")

        return self.opcodes[instr] * 100 + address
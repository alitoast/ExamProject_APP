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

        
    def _to_machine_code(self, source_lines):
        #
        # converte istruzioni in codice macchina
        #
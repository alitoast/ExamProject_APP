#
# Alice Macuz 
# SM3201385
#

from assembler import Assembler
import lmc
from interface import (
    get_input_values,
    choose_execution_mode,
    load_assembly_file,
    run_simulation
)
import os

def main():
    """
    Flusso principale del programma:
    - Carica e assembla un file .lmc
    - Chiede gli input (se necessari)
    - Esegue il programma in modalità scelta
    - Mostra il contenuto dell'output buffer
    """
    print("=== Simulatore Little Man Computer ===")

    # carica file assembly .lmc
    file_path, source_code = load_assembly_file()
    
    # assembla il codice in istruzioni macchina
    assembler = Assembler()
    try:
        memory = assembler.assemble(source_code)
    except Exception as e:
        print(f"Errore: Assemblaggio del codice fallito: {e}")
        return

    # verifica se il file non richiede input (dalla lista di esempio)
    filename = os.path.basename(file_path).lower()
    no_input_required = ["quine.lmc", "looping.lmc"]

    if filename in no_input_required:
        input_values = []
    else:
        input_values = get_input_values()
    
    # scelta modalità di esecuzione
    mode = choose_execution_mode()

    # esecuzione simulazione
    lmc_sim = run_simulation(memory, input_values, mode)

    print("=== Output Finale ===")
    print("Output queue:", lmc_sim.get_output())

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterruzione da tastiera. Uscita dal simulatore.")
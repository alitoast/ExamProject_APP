#
# Alice Macuz 
# SM3201385
#

from assembler import Assembler
import lmc

def get_input_values():
    #
    # prende valori dall'user 
    #
    while True:
        raw_input = input("Inserisci valori di input, separati dalla virgola se valori multipli: ").strip()
        if not raw_input:
            return []
        try:
            values = [int(x) for x in raw_input.split(",")]
            for val in values:
                if not (0 <= val <= 999):
                    raise ValueError()
            return values
        except ValueError:
            print("Input non valido. Inserire solo valori da 0 a 999, separati dalla virgola.")

def choose_execution_mode():
    #
    # scelta per esecuzione completa oppure step-by-step 
    #
    while True:
        mode = input("Modalità di esecuzione: [c]ompleta o [s]tep-by-step? ").strip().lower()
        if mode in ("c", "s"):
            return mode
        print("Scelta non valida. Inserire 'c' or 's'.")

def load_assembly_file():
    #
    # legge assembly dal file scelto 
    #
    while True:
        file_path = input("Inserisci percorso del file .lmc: ").strip()
        try:
            with open(file_path, "r") as f:
                return f.read()
        except FileNotFoundError:
            print(f"Errore: Il file '{file_path}' non è stato trovato. Riprova.")
        except Exception as e:
            print(f"Errore nella lettura del file: {e}. Riprova.")

def run_simulation(memory, input_values, mode):
    #
    # esegui LMC simulazione con input dato
    #
    lmc_sim = lmc.LMC(input_values=input_values)
    try:
        lmc_sim.load_program(memory)
        lmc_sim.execute(mode)
    except lmc.LMC.LMCError as e:
        print(f"Errore di runtime: {e}")
    except Exception as e:
        print(f"Errore inaspettato: {e}")
    return lmc_sim

def main():
    #
    # carica l'assembly, assembla il codice, scelta input,
    # scelta modlità esecuzione, esegue simulazione, display output finale
    #
    print("=== Simulatore Little Man Computer ===")
    source_code = load_assembly_file()
    
    assembler = Assembler()
    try:
        memory = assembler.assemble(source_code)
    except Exception as e:
        print(f"Errore: Assemblaggio del codice fallito: {e}")
        return
    
    input_values = get_input_values()
    mode = choose_execution_mode()
    lmc_sim = run_simulation(memory, input_values, mode)

    print("=== Output Finale ===")
    print("Output queue:", lmc_sim.get_output())

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterruzione da tastiera. Uscita dal simulatore.")
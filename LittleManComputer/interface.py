#
# Alice Macuz 
# SM3201385
#

"""
interface.py — Gestione dell'interfaccia utente per il simulatore LMC.
Questo modulo si occupa dell'interazione con l'utente:
- Riceve input numerici
- Chiede il file assembly da caricare
- Permette di scegliere la modalità di esecuzione
- Esegue il simulatore e gestisce eventuali errori
"""


from assembler import Assembler
import lmc

def get_input_values():
    """
    Chiede all'utente di inserire i valori di input
    da fornire al programma LMC.
    I valori devono essere numeri interi da 0 a 999, 
    separati da uno spazio.
    """
    while True:
        raw_input = input("Inserisci valori di input, separati da uno spazio se valori multipli: ").strip()

        if not raw_input:
            return [] # lista vuota se l'utente non inserisce nulla

        try:
            # converte i valori inseriti in interi
            values = [int(x) for x in raw_input.split(" ")]

            for val in values:
                if not (0 <= val <= 999):
                    raise ValueError()
            return values

        except ValueError:
            print("Input non valido. Inserire solo valori da 0 a 999, separati da uno spazio.")

def choose_execution_mode():
    """
    Chiede all'utente se eseguire il programma 
    in modalità completa o step-by-step. 
    Ritorna: 'c' o 's.
    """
    while True:
        mode = input("Modalità di esecuzione: [c]ompleta o [s]tep-by-step? ").strip().lower()
        if mode in ("c", "s"):
            return mode
        print("Scelta non valida. Inserire 'c' or 's'.")

def load_assembly_file():
    """
    Chiede all'utente il percorso del file .lmc da caricare.
    Verifica esistenza del file, estensione corretta e che sia leggibile. 
    """
    while True:
        file_path = input("Inserisci percorso del file .lmc: ").strip()

        if not file_path.lower().endswith(".lmc"):
            print("Errore: Il file deve avere estensione .lmc.")
            continue

        try:
            with open(file_path, "r") as f:
                source_code = f.read()
                return file_path, source_code

        except FileNotFoundError:
            print(f"Errore: Il file '{file_path}' non è stato trovato. Riprova.")

        except Exception as e:
            print(f"Errore nella lettura del file: {e}. Riprova.")

def run_simulation(memory, input_values, mode):
    """
    Esegue la simulazione LMC con i dati forniti.
    Carica il programma in memoria.
    Esegue secondo la modalità scelta.
    Gestisce eventuali errori durante l'esecuzione.
    """
    lmc_sim = lmc.LMC(input_values=input_values)

    try:
        lmc_sim.load_program(memory)
        lmc_sim.execute(mode)

    except lmc.LMC.LMCError as e:
        print(f"Errore di runtime: {e}")

    except Exception as e:
        print(f"Errore inaspettato: {e}")

    return lmc_sim
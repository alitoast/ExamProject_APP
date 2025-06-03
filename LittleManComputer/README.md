# Little Man Computer
##  Description

This project implements simulator for the **Little Man Computer (LMC)** using Python.

It features:
- An **assembler** that converts `.lmc` assembly files into machine code.
- A **virtual machine** that simulates memory, registers, branching, arithmetic, and I/O.
- A **command-line interface** to load programs, provide input, and run in normal or step-by-step mode.


---

## Project Structure

The project is organized into the following files:

* `main.py`: The main file that manages user interaction and the overall program flow.
* `assembler.py`: Contains the `Assembler` class that translates LMC assembly code into machine code.
* `lmc.py`: Contains the `LMC` class that implements the CPU of the Little Man Computer.

---

##  How to Run

###  Run the simulator

In terminal:

```bash
python main.py
```

### You will be prompted to:

1. Enter the path to your `.lmc` program
2. Enter input values (e.g. `4,5`)
3. Choose:

   * `c` for complete execution
   * `s` for step-by-step execution with memory state

---

## Example with `test.lmc`

### Run:

```bash
python main.py
```

**Input**:

```
=== Simulatore Little Man Computer ===
Inserisci percorso del file .lmc: LittleManComputer/tests/test.lmc
Inserisci valori di input, separati dalla virgola se valori multipli: 4,5
Modalità di esecuzione: [c]ompleta o [s]tep-by-step? c
```

**Output**:

```
=== Output Finale ===
Output queue: [9]
```

---
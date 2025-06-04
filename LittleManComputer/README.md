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

- `main.py`: Entry point of the simulator. It manages the overall program flow and coordinates the components.
- `interface.py`: Handles all user interaction, including input of values, selection of execution mode, and file loading.
- `assembler.py`: Contains the `Assembler` class, which converts `.lmc` assembly code into machine-readable memory.
- `lmc.py`: Contains the `LMC` class, which simulates the CPU architecture and executes the machine instructions.


---

##  How to Run

###  Run the simulator

In terminal:

```bash
python main.py
```

### You will be prompted to:

1. Enter the path to your `.lmc` program
2. Enter input values (e.g. `4 5`)
3. Choose:

   * `c` for complete execution
   * `s` for step-by-step execution with memory state

---

## Example with `test.lmc`

**test.lmc**
```
        INP         // Read first number
        STA TEMP    // Store it in TEMP
        INP         // Read second number
        ADD TEMP    // Add first number (from TEMP)
        OUT         // Output result
        HLT         // Halt program
TEMP    DAT 0       // Reserve memory for TEMP
```

### Execution:


```bash
python main.py
```

**When prompted:**:

```
=== Simulatore Little Man Computer ===
Inserisci percorso del file .lmc: tests/test.lmc
Inserisci valori di input, separati da uno spazio se valori multipli: 4 5
Modalità di esecuzione: [c]ompleta o [s]tep-by-step? c
```

**Expected Output:**

```
=== Output Finale ===
Output queue: [9]
```
---
## Notes

- Programs like `quine.lmc` and `looping.lmc` do not require input values.

- When executing `squares.lmc` finish the input line with 0, which signals the end of the computation.
  - Example: 8 9 0 (8 and 9 to square, 0 to end).

- Input values must be integers between 0 and 999.

- All assembly source files must have a .lmc extension
# Alice Macuz SM3201385

from copy import copy

class LMC:

    def __init__(self, input_values=None):
        self.ram = [0] * 100                  
        self.acc = 0                          # Accumulator
        self.pc = 0                           # Program counter
        self.input_buffer = input_values or []
        self.output_buffer = []
        self.flag = 0  # 1 if overflow or underflow, 0 otherwise
"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000

class CPU:
    """Main CPU class."""
    

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.sp = 7 #points to register not ram location
        self.running = False
        self.branchTable = {
            HLT : self.hlt,
            LDI : self.ldi,
            PRN : self.prn,
            MUL : self.mul,
            PUSH : self.push,
            POP : self.pop,
            CALL : self.call,
            RET : self.ret,
            ADD : self.add
        }

    def ram_read(self, MAR):
        return self.ram[MAR]
        
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR
    
    def push(self, a, b):
        reg = a
        value = self.reg[reg]
        self.reg[self.sp] -=1
        self.ram_write(self.reg[self.sp], value)
        self.pc += 2
    
    def pop(self, a, b):
        reg = a
        value = self.ram_read(self.reg[self.sp])
        self.reg[reg] = value
        self.reg[self.sp] +=1
        self.pc += 2

    def call(self, a, b):
        reg = a
        after = self.pc + 2
        self.pc = self.reg[reg]
        self.reg[self.sp] -= 1
        self.ram_write(self.reg[self.sp], after)

    def ret(self, a, b):
        self.pc = self.ram[self.reg[self.sp]]
        self.reg[self.sp] += 1

    def hlt(self, a = None , b = None):
        self.running = False

    def ldi(self, a, b):
        self.reg[a] = b
        self.pc += 3

    def prn(self, a, b = None):
        print(self.reg[a])
        self.pc += 2

    def add(self, a , b):
        self.alu('ADD', a, b)
        self.pc+=3

    def mul(self, a, b):
        self.reg[a] = self.reg[a] * self.reg[b]
        self.pc += 3

    def load(self, program):
        """Load a program into memory."""

        address = 0

        program = program
        with open(program) as f:
            for line in f:
                command = line.split('#')
                command = command[0].strip()
                if command == '':
                    continue
                command = int(command, 2)
                self.ram[address] = command
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.running = True
        # breakpoint()

        while self.running:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if IR in self.branchTable:
                self.branchTable[IR](operand_a, operand_b)
            else:
                print("Automatically Exited")
                self.hlt()
class Simulator:
   READ = 10
   WRITE = 11
   LOAD = 20
   STORE = 21
   ADD = 30
   SUBTRACT = 31
   MULTIPLY = 32
   DIVIDE = 33
   REMAINDER = 34
   BRANCH = 40
   BRANCH_NEG = 41
   BRANCH_ZERO = 42
   HALT = 43

   def __init__(self):
       self.accumulator = 0
       self.instructionCounter = 0
       self.operand = 0
       self.operationCode = 0
       self.instructionRegister = 0
       self.memory = [0] * 100

   def run_simulator(self):
       self.initializeRegisters()
       self.printInstructions()
       self.loadInstructions()
       self.execute()
       self.dump()

   def initializeRegisters(self):
       pass

   def printInstructions(self):
       display = """
       *** Welcome to Simpletron! ***
       *** Please enter your program one instruction ***
       *** (or data word) at a time into the input ***
       *** text field. I will display the location ***
       *** number and a question mark (?). You then ***
       *** type the word for that location. Enter ***
       *** -99999 to stop entering your program ***
       """
       print(display)

   def loadInstructions(self):
       counter = 0
       instructions_file = open('input_instructions.txt', 'r')
       instructions = instructions_file.readlines()
       #while counter < 100:
       for instruction in instructions:
           #instruction = int(input(f"{counter:02d} ? "))
           instruction = int(instruction)
           if (instruction == -99999 or counter>=100):
               break
           if self.validate(instruction):
               self.memory[counter] = instruction
               counter += 1
           else:
               print("Input invalid")

       print("*** Program loading completed ***")

   @staticmethod
   def validate(value):
       return -9999 <= value <= 9999

   def test_overflow(self):
       if not self.validate(self.accumulator):
           print("*** Fatal error. Accumulator overflow. ***")
           return True
       return False

   def execute(self):
       print("*** Program execution begins ***")
       input_file = open('input_file.txt', 'r')
       input_lines = input_file.readlines()
       line_no=0
       while self.instructionCounter < len(self.memory):
           self.instructionRegister = self.memory[self.instructionCounter]
           self.operationCode = self.instructionRegister // 100
           self.operand = self.instructionRegister % 100

           self.instructionCounter += 1
           if self.operationCode == self.READ:
               #print("Enter an integer: ", end='')
               self.memory[self.operand] = int(input_lines[line_no])
               line_no += 1
           elif self.operationCode == self.WRITE:
               print(f"Contents of {self.operand:02d} is {self.memory[self.operand]}")
           elif self.operationCode == self.LOAD:
               self.accumulator = self.memory[self.operand]
           elif self.operationCode == self.STORE:
               self.memory[self.operand] = self.accumulator
           elif self.operationCode == self.ADD:
               self.accumulator += self.memory[self.operand]
               if self.test_overflow():
                   return
           elif self.operationCode == self.SUBTRACT:
               self.accumulator -= self.memory[self.operand]
               if self.test_overflow():
                   return
           elif self.operationCode == self.MULTIPLY:
               self.accumulator *= self.memory[self.operand]
               if self.test_overflow():
                   return
           elif self.operationCode == self.DIVIDE:
               if self.memory[self.operand] == 0:
                   print("*** Fatal error. Attempt to divide by zero. ***")
                   return
               self.accumulator //= self.memory[self.operand]
           elif self.operationCode == self.REMAINDER:
               if self.memory[self.operand] == 0:
                   print("*** Fatal error. Attempt to divide by zero. ***")
                   return
               self.accumulator %= self.memory[self.operand]    
           elif self.operationCode == self.BRANCH:
               self.instructionCounter = self.operand
           elif self.operationCode == self.BRANCH_NEG:
               if self.accumulator < 0:
                   self.instructionCounter = self.operand
           elif self.operationCode == self.BRANCH_ZERO:
               if self.accumulator == 0:
                   self.instructionCounter = self.operand
           elif self.operationCode == self.HALT:
               print("*** Simpletron execution terminated ***")
               break
           else:
               print("*** Fatal error. Invalid operation code. ***")
               return

   def display_registers(self):
       print("REGISTERS:")
       print(f"{'Accumulator:':<24}{self.accumulator:+05d}")
       print(f"{'InstructionCounter:':<27}{self.instructionCounter:02d}")
       print(f"{'InstructionRegister:':<24}{self.instructionRegister:+05d}")
       print(f"{'OperationCode:':<27}{self.operationCode:02d}")
       print(f"{'Operand:':<27}{self.operand:02d}")

   def dump(self):
       self.display_registers()
       print("\nMEMORY:")
       print(" ", end='')
       for k in range(10):
           print(f"{k:7d}", end='')
       print()

       for k in range(10):
           print(f"{k * 10:02d}", end='')
           for i in range(10):
               print(f" {self.memory[k * 10 + i]:+05d}", end='')
           print()


#simulator = Simulator()
#simulator.run_simulator()

class SimulatorTest:
   def main(self, args):
       simpletron = Simulator()
       simpletron.run_simulator()

if __name__ == "__main__":
   test = SimulatorTest()
   test.main(None)

# libraries
from colorama import Style, Fore

# external files
import RF
import Solution

class Util:
    def __init__(self):
        pass

    def showBanner(self):
        print("Make Sure Your Input File is in test folder!")
    
class App:
    def __init__(self):
        self.rf = RF.RF()
        self.ut = Util()
        self.sol = None

        self.main()
        
    def main(self):
        if(self.rf.choice == 3):
            self.exit_program()
        elif(self.rf.choice == 1):
            self.rf.read_file()
        elif(self.rf.choice == 2):
            self.rf.generate_auto()
        
        self.sol = Solution.Solution(self.rf.matrix_size, self.rf.sequence, self.rf.matrix, self.rf.buffer_size)
        self.sol.main()
    
    def exit_program(self):
        exit(0)

if __name__ == "__main__":
    App()
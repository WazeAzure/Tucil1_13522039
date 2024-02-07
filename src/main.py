# libraries
from colorama import Style, Fore
import time
import multiprocessing
import numpy as np

# external files

class RF:
    def __init__(self):
        self.fname = ''
        self.buffer_size = 0
        self.matrix_size = None
        self.matrix = []
        self.sequence_size = 0
        self.sequence = []
    
    def showBanner(self):
        print("Make Sure Your Input File is in test folder!")
    
    def read_file(self):
        self.fname = "test/" + "test1.txt" # input('input filename: ')
        f = open(self.fname, 'r')
        f = f.read()
        f = f.split('\n')
        f[:] = [x for x in f if x.strip('\n')]

        # assign values
        self.buffer_size = int(f[0])
        self.matrix_size = list(map(lambda x: int(x), f[1].split(' ')))
        self.matrix = list(map(lambda x: x.split(' '), f[2:2+self.matrix_size[0]]))
        self.sequence_size = int(f[2+self.matrix_size[0]])
        for i in range(self.sequence_size):
            seq, val = f[2+self.matrix_size[0] + 1 + 2 *i], f[2+self.matrix_size[0] + 2 + 2 *i]
            self.sequence.append((seq.split(' '), int(val)))

class Solution:
    def __init__(self, matrix_size, sequence, matrix, buffer_size):
        self.row = matrix_size[0]
        self.col = matrix_size[1]
        self.sequence = sequence
        self.matrix = matrix
        self.ans_pool = []
        self.max_depth = buffer_size
        self.max_score = 0
        self.max_coor = []
        visited = np.zeros((self.row, self.col))

        if(buffer_size > sum([x[1] for x in sequence])):
            self.max_depth = sum([x[1] for x in sequence])

        start_t = time.time()
        self.brute_force(0, 0, True, "", 0, [], visited)
        self.check_ans()
        end_t = time.time()

        self.time_elapsed = end_t - start_t

        self.show_banner()
        self.show_answer()
    
    def brute_force(self, row, col, b, ans, depth, coor, visited):
        if (depth == self.max_depth): # basis max depth
            # print("called")
            self.ans_pool.append((ans, coor))
            return
        
        

        if (b): # b = True -> Horizontal 
            for j in range(self.col):
                visited2 = np.copy(visited)
                if(visited2[row][j] == 0):
                    visited2[row][j] = 1
                    ans2 = ans + self.matrix[row][j] + " "
                    self.brute_force(row, j, not b, ans2, depth+1, [*coor, (row, j)], visited2)
        else: # b = False -> Vertical
            for i in range(self.row):
                visited2 = np.copy(visited)
                if(visited2[i][col] == 0):
                    visited2[i][col] = 1
                    ans2 = ans + self.matrix[i][col] + " "
                    
                    self.brute_force(i, col, not b, ans2, depth+1, [*coor, (i, col)], visited2)
    
    def printMatrix(self, visited):
        for x in list(map(lambda x: " ".join(str(x)), visited)):
            print(x)
        print("=====================================")
    
    def check_ans(self):
        max_score = 0
        max_coor = []
        print(self.ans_pool)
        for x in self.ans_pool:
            temp_score = 0
            for i in range (len(self.sequence)):
                s = " ".join(self.sequence[i][0])
                # print(s, " | ", x)
                if s in x[0]:
                    # print(s, " | ", x)
                    temp_score += self.sequence[i][1]
            
            # print(temp_score)
            if(temp_score > max_score):
                max_score = temp_score
                max_coor = x[1]

        self.max_score = max_score
        self.max_coor = max_coor
    
    def show_banner(self):
        print("========================================")
        print("|               SOLUTION               |")
        print("========================================")
        
    def show_answer(self):
        print("Max score:\t", self.max_score)
        print("Sequence:\t", " ".join(list(map(lambda x: self.matrix[x[0]][x[1]], self.max_coor))))
        print("Coordinates:\n", "\n".join(list(map(lambda x: "("+str(x[0])+", "+str(x[1])+")", self.max_coor))))
        print("Time elapsed:\t", self.time_elapsed, "s")
        choice = input("Apakah anda ingin menyimpan solusi? (y/n)\n> ")

        if(choice == 'y'):
            self.saveToFile()
    
    def saveToFile(self):
        fname = "test/" + "solution-test1.txt"
        f = open(fname, "w")

        f.write("========================================\n")
        f.write("|               SOLUTION               |\n")
        f.write("========================================\n")
        f.write("Max score:\t{}\n".format(self.max_score))
        f.write("Sequence:\t{}\n".format(" ".join(list(map(lambda x: self.matrix[x[0]][x[1]], self.max_coor)))))
        f.write("Coordinates:\n{}\n".format("\n".join(list(map(lambda x: "("+str(x[0])+", "+str(x[1])+")", self.max_coor)))))
        f.write("Time elapsed:\t{} s".format(self.time_elapsed))


class Util:
    def __init__(self):
        pass

    def showBanner(self):
        print("Make Sure Your Input File is in test folder!")
    

class App:
    def __init__(self):

        self.init()

        self.rf = RF()
        self.ut = Util()
        # self.tt = test.Test() # unit testing
        self.main()
        self.sol = Solution(self.rf.matrix_size, self.rf.sequence, self.rf.matrix, self.rf.buffer_size)

    def init(self):
        choice = ("Apakah Anda ingin generate otomatis? (y/n)\n> ")
        if(choice == 'n'):
            return False
        elif(choice == 'y'):
            return True
        else:
            return 'x'
        
    def main(self):
        self.rf.read_file()
        
        # solution

if __name__ == "__main__":
    App()
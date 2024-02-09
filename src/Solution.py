import numpy as np
import time
import multiprocessing
import os

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
        self.time_elapsed = 0
        self.abs_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        print("max depth dari dalam:", self.max_depth)
        if(buffer_size > sum([len(x[0]) for x in sequence])):
            self.max_depth = sum([x[1] for x in sequence])
    
    def main(self):
        visited = np.zeros((self.row, self.col))

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
        elif (depth > self.max_depth):
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
        print("checK_ans clalled")
        max_score = float('-inf')
        max_coor = []
        # print(self.ans_pool)
        for x in self.ans_pool:
            isExist = False
            temp_score = 0
            for i in range (len(self.sequence)):
                s = " ".join(self.sequence[i][0])
                # print(s, " | ", x)
                if s in x[0]:
                    # print(s, " | ", x)
                    temp_score += self.sequence[i][1]
                    isExist = True
            
            # print(temp_score)
            if(temp_score > max_score and isExist):
                max_score = temp_score
                max_coor = x[1]
        if(max_score == float('-inf')):
            self.max_score = 0
        else:
            self.max_score = max_score
        self.max_coor = max_coor
    
    def show_banner(self):
        print("========================================")
        print("|               SOLUTION               |")
        print("========================================")
        
    def show_answer(self):
        print("Max score:\t", self.max_score)
        print("Sequence:\t", " ".join(list(map(lambda x: self.matrix[x[0]][x[1]], self.max_coor))))
        print("Coordinates:\n", "\n".join(list(map(lambda x: "("+str(x[1]+1)+", "+str(x[0]+1)+")", self.max_coor))))
        print("Time elapsed:\t", round(self.time_elapsed * 1000, 2), "ms")
        
    def saveToFile(self, fname):
        fname = self.abs_path + "/test/solution-" + fname #"solution-test1.txt"
        f = open(fname, "w")

        f.write("========================================\n")
        f.write("|               SOLUTION               |\n")
        f.write("========================================\n")
        f.write("Max score:\t{}\n".format(self.max_score))
        f.write("Sequence:\t{}\n".format(" ".join(list(map(lambda x: self.matrix[x[0]][x[1]], self.max_coor)))))
        f.write("Coordinates:\n{}\n".format("\n".join(list(map(lambda x: "("+str(x[1]+1)+", "+str(x[0]+1)+")", self.max_coor)))))
        f.write("Time elapsed:\t{} ms".format(round(self.time_elapsed*1000, 2)))

        print(f"File saved in {fname}")

        return fname
import random
import numpy as np

class RF:
    def __init__(self):
        self.fname = ''
        self.buffer_size = 0
        self.matrix_size = None
        self.matrix = []
        self.sequence_size = 0
        self.sequence = []
        self.choice = 0
        
        self.input_prompt()
    
    def input_prompt(self):
        choice = input("Apakah Anda ingin generate otomatis? (y/n)\n> ")
        if(choice == 'n'):
            self.choice = 1
        elif(choice == 'y'):
            self.choice = 2
        else:
            self.choice = 3
        
    
    def showBanner(self):
        print("Make Sure Your Input File is in test folder!")
    
    def generate_auto(self):
        token_n = input("Masukkan jumlah token\n> ")
        token = np.array(input("Masukkan token\n> ").split(' '))
        buffer_size = int(input("Masukkan ukuran buffer\n> "))
        matrix_size = list(map(lambda x: int(x), input("Masukkan ukuran matriks (row, col)\n> ").split(' ')))
        seq_size = int(input("Masukkan banyak sequence\n> "))
        seq_len = int(input("Masukkan maksimum panjang sequence\n> "))

        self.buffer_size = buffer_size
        self.matrix_size = matrix_size
        self.sequence_size = seq_size

        self.matrix = np.random.randint(0, token_n, size=(matrix_size[0], matrix_size[1]))
        self.matrix = token[self.matrix]
        print(self.matrix)

        rand_seq_size = np.random.randint(2, seq_len+1, size=(seq_size))

        self.sequence = []

        for x in rand_seq_size:
            self.sequence.append((list(token[(np.random.randint(0, token_n, size=(x)))]), random.randint(10, 50)))
        
        for x in self.sequence:
            print(" ".join(x[0]), "|", x[1])

    
    def read_file(self):
        self.fname = "test/" + input('input filename\n> ')
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
import main

class Test:
    def __init__(self):
        self.app = main.App()

        # self.RF_test(self.app.rf)
        self.SOL_test(self.app.sol)

    def RF_test(self, Part):
        print(Part.buffer_size)
        print(Part.matrix_size)
        print(Part.matrix)
        print(Part.sequence_size)
        print(Part.sequence)
    
    def SOL_test(self, Part):
        print(Part.row)
        print(Part.col)
        print(Part.sequence)
        print(Part.matrix)
        print(Part.visited)
        print((Part.ans_pool))
        print(Part.max_depth)
        print(Part.max_score)
        print(Part.max_coor)

if __name__ == "__main__":
    Test()
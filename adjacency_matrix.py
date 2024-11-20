class Matrix:
    def __init__(self,rows: int,cols: int) -> None:
        self.matrix = [[0 for col in range(cols)] for row in range(rows)]
        self.rows = rows
        self.cols = cols
    
    def manual_input(self) -> None:
        for y in range(self.rows):
            for x in range(self.cols):
                while True:
                    try:
                        c = int(input(f'number ({x}, {y}): '))
                    except TypeError:
                        print("Invalid value.")
                    else:
                        self.matrix[y][x] = c
                        break
    
    def automatic_input(self, coords: tuple, val: int) -> None:
        pass

    def get_matrix(self) -> list:
        return self.matrix

    def __str__(self) -> str:
        return_var = ''
        for i in self.matrix:
            return_var += str(i) + '\n'
        return return_var
    
def get_connections():
    go = True

def main():
    t_m = Matrix(4,3)
    t_m.manual_input()
    print(t_m)

if __name__ == '__main__':
    main()
from random import randint
from calc import calc_min, get_index

# class game field manage - tracer
class Field:
    def __init__(self, width, height):
        self.List = []
        self.generate_zero_field(width, height)

    # create new game field matrix with zero elements
    def generate_zero_field(self, width, height):
        list = []
        for i in range(0, height):
            list.append([])
            for j in range(0, width):
                list[i].append(0)
        self.List = list

    # print new game field matrix
    def showField(self):
        for i in self.List:
            print(i)

# class game field manage - mines field
class mine_Field(Field):
    def __init__(self, width, height, mines):
        super().__init__(width, height)
        self.List = []
        self.width = width
        self.height = height
        self.mines = mines
        self.generate_zero_field(width, height)
        self.place_min(mines)
        self.addNumber()

    # pace mines in game field matrix
    def place_min(self, mines):

        while mines != 0:
            i = randint(0, self.height - 1)
            j = randint(0, self.width - 1)
            if self.List[i][j] == 0:
                self.List[i][j] = -1
                mines -= 1

    # calculate mine around every cell
    def addNumber(self):
        for i, var_i in enumerate(self.List):
            for j, var_j, in enumerate(var_i):
                if var_j == -1:
                    continue
                else:
                    self.List[i][j] = calc_min(self.List, i, j, self.width, self.height, -1)

    # create new game field matrix  without minimum zero field
    def set_new_field(self, width, height, mines):
        self.width = width
        self.height = height
        self.mines = mines
        self.generate_zero_field(width, height)
        self.place_min(mines)
        self.addNumber()

    # create new game field matrix with minimum zero field
    def set_new_field_by_cell(self, i, j, width, height, mines):
        self.width = width
        self.height = height
        self.mines = mines
        self.generate_zero_field(width, height)
        self.List[i][j] = 1
        self.generate_no_zero(i, j)
        self.addDefense()
        self.place_min(mines)
        self.set_zero()
        self.addNumber()

    # add minimum zero field to matrix
    def generate_no_zero(self, i, j):
        num_mines = int(self.mines / 20 + 1)
        while num_mines != 0:
            way = randint(1, 8)
            new_i, new_j = get_index(i, j, way)
            if 0 <= new_i < self.height and 0 <= new_j < self.width:
                i = new_i
                j = new_j
                if self.List[i][j] == 0:
                    self.List[i][j] = 1
                    num_mines -= 1

    # set zero to minimum zero field to matrix after place number
    def set_zero(self):
        for i, var_i in enumerate(self.List):
            for j, var_j, in enumerate(var_i):
                if var_j == 1 or var_j == 2:
                    self.List[i][j] = 0

    # add defense zero to minimum for no break
    def addDefense(self):
        for i, var_i in enumerate(self.List):
            for j, var_j, in enumerate(var_i):
                if var_j == 0:
                    self.set_one(i, j, i + 1, j)
                    self.set_one(i, j, i - 1, j)
                    self.set_one(i, j, i, j + 1)
                    self.set_one(i, j, i, j - 1)
                    self.set_one(i, j, i + 1, j + 1)
                    self.set_one(i, j, i + 1, j - 1)
                    self.set_one(i, j, i - 1, j + 1)
                    self.set_one(i, j, i - 1, j - 1)

    # set one to minimum zero field to matrix after place minimum zero field
    def set_one(self, ii, jj, i, j):
        if 0 <= i < self.height and 0 <= j < self.width:
            if self.List[i][j] == 1:
                self.List[ii][jj] = 2
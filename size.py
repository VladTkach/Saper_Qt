# class to save size about interface
class Size:
    def __init__(self, level):
        self.level = level
        self.set_size(self.level)
    # set new size to interface by level
    def set_size(self, level):
        match level:
            case 1:
                self.mines = 10
                self.cell_width = 10
                self.cell_height = 8
                self.cell_size = 50

            case 2:
                self.mines = 40
                self.cell_width = 18
                self.cell_height = 14
                self.cell_size = 40
            case 3:
                self.mines = 99
                self.cell_width = 24
                self.cell_height = 20
                self.cell_size = 30

        self.cell = self.cell_height * self.cell_width
        self.free_cell = self.cell - self.mines
        self.width = self.cell_width * self.cell_size - 10
        self.height = self.cell_height * self.cell_size + 100

    # print interface sizes
    def showElements(self):
        print(self.mines)
        print(self.free_cell)
        print(self.cell_width)
        print(self.cell_height)
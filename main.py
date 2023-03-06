import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QGridLayout, QButtonGroup, QApplication, QMainWindow, QPushButton, QLabel, QAction
from PyQt5.QtCore import QEvent, Qt, QTimer, QSize
from PyQt5.QtGui import QFont, QIcon

from size import Size
from field import Field, mine_Field
from fileWork import fileWork
from calc import calc_min, is_cell


# basic class for the interface and work with it
class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.play = False
        self.level = 1
        self.count = 0
        self.flag = False
        self.add_UI()
        self.start()

    # reaction to the click of the playing field button
    def callback(self, btn):
        in_i, in_j = self.getIndex(self.buttons.id(btn))
        if self.trace.List[in_i][in_j] != 2 and self.trace.List[in_i][in_j] != 3 and self.trace.List[in_i][in_j] != 1:
            if not self.flag:
                self.flag = True
            if not self.play:
                self.play = True
                self.mine_field.set_new_field_by_cell(in_i, in_j, self.size.cell_width, self.size.cell_height,
                                                      self.size.mines)
            if self.mine_field.List[in_i][in_j] == -1:
                self.lose()
            elif self.mine_field.List[in_i][in_j] == 0:
                self.open_zero(in_i, in_j)
            else:
                btn.setText(str(self.mine_field.List[in_i][in_j]))
                self.trace.List[in_i][in_j] = 1
                self.setBtn_on(self.buttons.button(in_i * self.size.cell_width + in_j))
                self.size.free_cell -= 1
                self.if_Win()
                btn.setEnabled(False)

    # get coordinates by index
    def getIndex(self, index):
        in_i = int(index / self.size.cell_width)
        in_j = index - in_i * self.size.cell_width
        return in_i, in_j

    # processing of different types of pressing
    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.RightButton:
                index = self.buttons.id(source)
                in_i, in_j = self.getIndex(index)
                if self.trace.List[in_i][in_j] == 0:
                    self.trace.List[in_i][in_j] = 2
                    source.setIcon(QtGui.QIcon('flag.png'))
                    self.size.mines -= 1
                    self.mine_label.setText(str(self.size.mines))
                    if not self.flag:
                        self.flag = True
                elif self.trace.List[in_i][in_j] == 2:
                    self.trace.List[in_i][in_j] = 0
                    source.setIcon(QtGui.QIcon(None))
                    self.size.mines += 1
                    self.mine_label.setText(str(self.size.mines))
        elif event.type() == QEvent.MouseButtonDblClick:
            index = self.buttons.id(source)
            in_i, in_j = self.getIndex(index)
            text = self.buttons.button(index).text()
            if text != "":
                if int(text) == calc_min(self.trace.List, in_i, in_j, self.size.cell_width, self.size.cell_height, 2):
                    self.open_around(in_i, in_j)

        return False

    # open cell around by coordinates
    def open_around(self, i, j):
        for x in range(-1, 2):
            for y in range(-1, 2):
                if is_cell(i + x, j + y, self.size.cell_width, self.size.cell_height):
                    self.callback(self.buttons.button((i + x) * self.size.cell_width + (j + y)))

    # open cells if click in zero cell
    def open_zero(self, i, j):
        if self.size.cell_width > j >= 0 and self.size.cell_height > i >= 0 and self.trace.List[i][j] != 1:
            if self.mine_field.List[i][j] == 0:
                self.trace.List[i][j] = 1
                self.size.free_cell -= 1
                self.if_Win()
                self.buttons.button(i * self.size.cell_width + j).setIcon(QtGui.QIcon(None))
                self.buttons.button(i * self.size.cell_width + j).setEnabled(False)
                self.setBtn_on(self.buttons.button(i * self.size.cell_width + j))
                self.open_zero(i, j + 1)
                self.open_zero(i, j - 1)
                self.open_zero(i + 1, j)
                self.open_zero(i - 1, j)
                self.open_zero(i - 1, j + 1)
                self.open_zero(i - 1, j - 1)
                self.open_zero(i + 1, j + 1)
                self.open_zero(i + 1, j - 1)

            elif self.mine_field.List[i][j] > 0:
                self.buttons.button(i * self.size.cell_width + j).setText(str(self.mine_field.List[i][j]))
                self.buttons.button(i * self.size.cell_width + j).setIcon(QtGui.QIcon(None))
                self.buttons.button(i * self.size.cell_width + j).setEnabled(True)
                self.setBtn_on(self.buttons.button(i * self.size.cell_width + j))
                self.trace.List[i][j] = 1
                self.size.free_cell -= 1
                self.if_Win()

    # checking the victory
    def if_Win(self):
        if self.size.free_cell == 0:
            self.mine_label.setText("Win")
            self.flag = False
            self.play = False
            self.file.record.setRecord(self.level, self.count)
            self.file.updateFile()
            self.setNewRecordMenu()
            self.block_area()

    # data processіng if lose
    def lose(self):
        self.mine_label.setText("Lose")
        self.flag = False
        self.play = False
        for i in range(0, self.size.cell):
            in_i, in_j = self.getIndex(i)
            if self.mine_field.List[in_i][in_j] == -1:
                self.buttons.button(i).setIcon(QtGui.QIcon('min.png'))
        self.block_area()

    # blocking the playing field after winning or losing
    def block_area(self):
        for i in range(0, self.size.cell):
            in_i, in_j = self.getIndex(i)
            self.trace.List[in_i][in_j] = 3

    # change current time
    def showTime(self):
        if self.flag:
            self.count += 1
            text = str(self.count / 10)
            self.time_label.setText(text)

    # Restart game
    def Restart(self):
        self.flag = False
        self.play = False
        self.count = 0
        self.time_label.setText(str(self.count / 10))
        self.mine_label.setText(str(self.size.mines))

        self.clear()
        self.start()

    # Window style
    def setWindow(self):
        self.setWindowIcon(QIcon("min.png"))
        self.setWindowTitle("Minesweeper")
        self.setFixedWidth(self.size.width)
        self.setFixedHeight(self.size.height)

    # game field button style
    def setBtn(self, button):
        button.setFixedHeight(self.size.cell_size)
        button.setFixedWidth(self.size.cell_size)
        button.setIconSize(QSize(self.size.cell_size, self.size.cell_size))
        button.setStyleSheet("color: black;"
                             "background-color: grey;"
                             "font: 20px;"
                             "margin: 0;"
                             "border-style: outset;"
                             "border: 1px solid")
        button.setCheckable(False)

    # game field button style on click
    def setBtn_on(self, button):
        button.setStyleSheet("color: black;"
                             "background-color: white;"
                             "font: 20px;"
                             "margin: 0;"
                             "border-style: outset;"
                             "border: 1px solid")

    # restart button style
    def setRestartBTN(self):
        self.restart_button.setText("Restart")
        self.restart_button.setGeometry(int(self.size.width / 2 - 50), 40, 100, 50)
        self.restart_button.setStyleSheet("QPushButton {"
                                          "background-color: white;"
                                          "border-style: outset;"
                                          "font: bold 20px;"
                                          "border-color: #2752B8;"
                                          "}"
                                          "QPushButton:hover {"
                                          "background-color: lightgreen;")

    # group button/game field style
    def setGroupBtn(self):
        index = 0
        for i, val in enumerate(self.mine_field.List):
            for j, val_j in enumerate(val):
                button = QtWidgets.QPushButton()
                self.setBtn(button)
                self.Layout.addWidget(button, i, j)
                self.buttons.addButton(button)
                self.buttons.setId(button, index)
                button.installEventFilter(self)
                index += 1

    # widget style
    def setWidget(self):
        self.widget.setStyleSheet("background-color: rgb(220, 220, 220);")
        self.widget.setGeometry(0, 0, self.size.width, 100)

    # widget game field style
    def setArea(self):
        self.Layout.setSpacing(0)
        self.L_widget.setGeometry(0, 100, self.size.width, self.size.height - 100)

    # timer style
    def setTimeLabel(self):
        self.time_label.setText(str(self.count))
        self.time_label.setGeometry(20, 40, 100, 50)
        self.time_label.setFont(QFont('Arial', 20))

    # timer connect to {showTime}
    def setTimer(self):
        self.timer.timeout.connect(self.showTime)
        self.timer.start(100)

    # sum of mines style
    def setMineLabel(self):
        self.mine_label.setText(str(self.size.mines))
        self.mine_label.setFont(QFont('Arial', 20))
        self.mine_label.setGeometry(self.size.width - 100, 40, 100, 50)

    # create level menu
    def setLevelMenu(self):
        level1 = QAction('&Level - 1', self)
        level1.triggered.connect(self.level_1Call)
        level1.setShortcut('Ctrl+1')

        level2 = QAction('&Level - 2', self)
        level2.triggered.connect(self.level_2Call)
        level2.setShortcut("Ctrl+2")

        level3 = QAction('&Level - 3', self)
        level3.triggered.connect(self.level_3Call)
        level3.setShortcut('Ctrl+3')

        self.levelMenu.addAction(level1)
        self.levelMenu.addAction(level2)
        self.levelMenu.addAction(level3)

    # create menu
    def setMenu(self):
        self.levelMenu = self.menuBar.addMenu('&Level')
        self.RecordMenu = self.menuBar.addMenu('&Record')

        self.setLevelMenu()
        self.setRecordMenu()

    # create record menu
    def setRecordMenu(self):
        self.level_1 = QAction("level_1: " + str(self.file.record.record_lv1 / 10), self.RecordMenu)
        self.level_2 = QAction("level_2: " + str(self.file.record.record_lv2 / 10), self.RecordMenu)
        self.level_3 = QAction("level_3: " + str(self.file.record.record_lv3 / 10), self.RecordMenu)

        cancel = QAction('&Cancel record', self)
        cancel.triggered.connect(self.cancelRecord)

        self.RecordMenu.addAction(self.level_1)
        self.RecordMenu.addAction(self.level_2)
        self.RecordMenu.addAction(self.level_3)
        self.RecordMenu.addAction(cancel)

    # update record menu
    def setNewRecordMenu(self):
        self.level_1.setText("level_1: " + str(self.file.record.record_lv1 / 10))
        self.level_2.setText("level_2: " + str(self.file.record.record_lv2 / 10))
        self.level_3.setText("level_3: " + str(self.file.record.record_lv3 / 10))

    # cancel current records
    def cancelRecord(self):
        self.file.record.setZero()
        self.file.zeroFile()
        self.setNewRecordMenu()

    # level - 1 reaction on click in level menu
    def level_1Call(self):
        self.level = 1
        self.Restart()

    # level - 2 reaction on click in level menu
    def level_2Call(self):
        self.level = 2
        self.Restart()

    # level - 3 reaction on click in level menu
    def level_3Call(self):
        self.level = 3
        self.Restart()

    # generate new game fild matrix
    def generate_Area(self, level):
        self.size.set_size(level)
        self.trace = Field(self.size.cell_width, self.size.cell_height)
        self.mine_field = mine_Field(self.size.cell_width, self.size.cell_height, self.size.mines)

    # clear game fild matrix
    def clear(self):
        for i in range(0, self.size.cell):
            self.buttons.button(i).setEnabled(True)
            self.buttons.removeButton(self.buttons.button(i))

        for i in range(0, self.size.cell):
            self.Layout.removeWidget(self.Layout.itemAt(0).widget())

    # start new level or start playing + set style of elements
    def start(self):
        self.size = Size(self.level)
        self.generate_Area(self.level)
        self.setArea()
        self.setMineLabel()
        self.setTimeLabel()
        self.setWindow()
        self.setWidget()
        self.setRestartBTN()
        self.setGroupBtn()

    # add window elements and parts
    def add_UI(self):
        self.widget = QtWidgets.QWidget(self)
        self.restart_button = QPushButton(self.widget)
        self.restart_button.pressed.connect(self.Restart)
        self.time_label = QLabel(self.widget)
        self.mine_label = QLabel(self.widget)
        self.timer = QTimer(self.widget)
        self.L_widget = QtWidgets.QWidget(self)
        self.Layout = QGridLayout(self.L_widget)
        self.buttons = QButtonGroup(self)
        self.buttons.buttonClicked.connect(self.callback)
        self.setTimer()
        self.menuBar = self.menuBar()
        self.file = fileWork("record.txt")
        self.setMenu()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

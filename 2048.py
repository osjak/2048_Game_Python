#!/usr/bin/python
import curses
from random import randint, random
import time
import sys

class Grid():
    def __init__(self, size):
        self.score = Score()
        self.items = ['', '2', '4', '8', '16', '32', '64', '128', '256', '512', '1M', '2M', '4M']
        self.size = size
        self._generateGrid()
        self._generateItems(2)
        self.score.setScore(0)

    def _generateGrid(self):
        self.map = [[0 for j in range(self.size)] for j in range(self.size)]

    def _generateItems(self, nItems):
        itemsCount = 0
        freeSpace = 0

        for i in range(self.size):
            for j in range(self.size):
                if self.map[i][j] == 0:
                    freeSpace += 1
        if freeSpace == 0:
            self.gameOver()

        while itemsCount < nItems:
            x = randint(0, self.size - 1)
            y = randint(0, self.size - 1)
            if self.map[x][y] == 0:
                self.map[x][y] = 1 if random() < .75 else 2
                itemsCount += 1
                self.score.incrScore(10)

    def changeDirection(self, ch):
        if ch == curses.KEY_LEFT :
            self.goLeft()
        if ch == curses.KEY_RIGHT :
            self.goRight()
        if ch == curses.KEY_UP :
            self.goUp()
        if ch == curses.KEY_DOWN :
            self.goDown()
        self._generateItems(1)

    def goLeft(self):
        newMap = []
        for i in range(self.size):
            row = self.map[i]
            newRow = [val for val in row if val != 0]

            for j in range(len(newRow) - 1):
                if newRow[j] == newRow[j+1]:
                    del(newRow[j])
                    newRow.append(0)
                    newRow[j] += 1

            for j in range(self.size - len(newRow)):
                newRow.append(0)
            self.map[i] = newRow

    def goRight(self):
        for i in range(self.size):
            row = self.map[i]
            newRow = [val for val in row if val != 0]

            for j in range(len(newRow) - 1, 0, -1):
                if newRow[j] == newRow[j-1]:
                    del(newRow[j])
                    newRow.insert(0, 0)
                    newRow[j] += 1

            for j in range(self.size - len(newRow)):
                newRow.insert(0, 0)
            self.map[i] = newRow

    def goUp(self):
        for k in range(self.size):
            col = []
            newCol = []
            newRow = []
            for i in range(self.size):
                col.append(self.map[i][k])

            newCol = [val for val in col if val != 0]
            for j in range(len(newCol) - 1):
                if newCol[j] == newCol[j+1]:
                    del(newCol[j])
                    newCol.append(0)
                    newCol[j] += 1

            for j in range(self.size - len(newRow)):
                newCol.append(0)

            for j in range(self.size):
                self.map[j][k] = newCol[j]
            
    def goDown(self):
        for k in range(self.size):
            col = []
            newCol = []
            newRow = []
            for i in range(self.size):
                col.append(self.map[i][k])

            newCol = [val for val in col if val != 0]
            for j in range(len(newCol) - 1, 0, -1):
                if newCol[j] == newCol[j-1]:
                    del(newCol[j])
                    newCol.insert(0, 0)
                    newCol[j] += 1

            for j in range(self.size - len(newCol)):
                newCol.insert(0, 0)

            for j in range(self.size):
                self.map[j][k] = newCol[j]

    def renderChessboard(self, screen, length):
        line = 2
        sep_v = "|"
        sep_h = "-"
        for i in range(self.size):
            screen.addstr(line, 0, sep_h * length * self.size)
            line += 1
            for j in range(3):
                for k in range(self.size + 1):
                    screen.addstr(line, (k * length), sep_v)
                line += 1
        screen.addstr(line, 0, sep_h * length * self.size)

    def render(self, screen, length):
        for i in range(self.size):
            row = ' '
            for j in range(self.size):
                row += '{0:^{1}}'.format(self.items[self.map[i][j]], length)
            screen.addstr((i*4) + 4, 0, row)
        self.renderChessboard(screen, length)

    def gameOver(self):
        print("Game Over !")
        sys.exit()

class Score:
    def __init__(self):
        self.score = 0
        self.scoreStr = 'Score : 0'

    def incrScore(self, value):
        self.score += value
        self.updateStr()

    def decrScore(self, value):
        self.score -= value
        self.updateStr()

    def getScore(self):
        return self.score

    def setScore(self, sc):
        self.score = sc
        self.updateStr()

    def updateStr(self):
        self.scoreStr = 'Score : ' + str(self.getScore())

    def render(self, screen):
        screen.addstr(0, 0, self.scoreStr)

def main(screen):
    screen.timeout(0)
    grid = Grid(4)

    while(True):
        ch = screen.getch()
        if ch != -1:
            grid.changeDirection(ch)
        grid.score.render(screen)
        grid.render(screen, 8)
        screen.refresh()
        time.sleep(0.4)

curses.wrapper(main)

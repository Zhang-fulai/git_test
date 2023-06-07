import random
import tkinter as tk
from tkinter import messagebox as msgbox
from typing import List


class Lifes:

    def __init__(self, rows=36, cols=36):
        self.row = rows + 2
        self.col = cols + 2
        self.items = [[0] * self.col for _ in range(self.row)]
        self.history = []
        self.historySize = 30
        self.running = False
        self.runningSpeed = 100

    def rndinit(self, rate=0.1):
        self.history = []
        for i in range(self.row):
            for j in range(self.col):
                rnd = random.random()
                if rnd > 1 - rate:
                    self.items[i][j] = 1

    def reproduce(self):
        new = [[0] * self.col for _ in range(self.row)]
        self.add_history()
        if len(self.history) > self.historySize:
            self.history.pop(0)
        for i in range(self.row):
            for j in range(self.col):
                if i * j == 0 or i == self.row - 1 or j == self.col - 1:
                    new[i][j] = 0
                else:
                    lifes = 0
                    for m in range(i - 1, i + 2):
                        for n in range(j - 1, j + 2):
                            if m == i and n == j:
                                continue
                            lifes += self.items[m][n]
                    if self.items[i][j]:
                        if lifes == 2 or lifes == 3:
                            new[i][j] = 1
                        else:
                            new[i][j] = 0
                    else:
                        if lifes == 3:
                            new[i][j] = 1
        for idx, narray in enumerate(new):
            self.items[idx] = narray

    def is_stable(self):
        if len(self.history) < self.historySize:
            return False
        arr = []
        for i in self.history:
            if i not in arr:
                arr.append(i)
        if len(arr) < 10:
            return True

    def add_history(self, Items=None):
        arr = []
        if Items == None:
            Items = self.items[:]
        for item in Items:
            b = 0
            for i, n in enumerate(item[::1]):
                b += n * 2 ** i
            arr.append(b)
        self.history.append(arr)


def drawCanvas():
    global tv, rect
    tv = tk.Canvas(window, width=window.winfo_width(), height=window.winfo_height())
    tv.pack(side="top")
    for i in range(36):
        coord = 40, 40, 760, i * 20 + 40
        tv.create_rectangle(coord)
        coord = 40, 40, i * 20 + 40, 760
        tv.create_rectangle(coord)
    coord = 38, 38, 760, 760
    tv.create_rectangle(coord, width=2)
    coord = 39, 39, 760, 760
    tv.create_rectangle(coord, width=2)
    coord = 38, 38, 762, 762
    tv.create_rectangle(coord, width=2)

    R, XY = 8, [50 + i * 20 for i in range(36)]
    rect = [[0] * 36 for _ in range(36)]
    for i, x in enumerate(XY):
        for j, y in enumerate(XY):
            rect[i][j] = tv.create_rectangle(x - R, y - R, x + R, y + R, tags=('imgButton1'))
            tv.itemconfig(rect[i][j], fill='lightgray', outline='lightgray')
    tv.tag_bind('imgButton1', '<Button-1>', on_Click)


def drawLifes():
    R, XY = 8, [50 + i * 20 for i in range(36)]
    if Life.running:
        for i, x in enumerate(XY):
            for j, y in enumerate(XY):
                if Life.items[i + 1][j + 1]:
                    tv.itemconfig(rect[i][j], fill='blue', outline='blue')
                else:
                    tv.itemconfig(rect[i][j], fill='lightgray', outline='lightgray')
        tv.update()
        Life.reproduce()
        if Life.is_stable():
            Life.running = False
            if sum(sum(Life.items, [])):
                msgbox.showinfo('Message', '生命繁殖与湮灭进入稳定状态！！！')
            else:
                msgbox.showinfo('Message', '生命全部湮灭，进入死亡状态！！！')
    window.after(Life.runningSpeed, drawLifes)


def StartLife():
    if sum(sum(Life.items, [])):
        Life.history = []
        Life.running = True
    else:
        msgbox.showinfo('Message', '请点击小方块填入生命细胞，或者使用随机功能！')


def BreakLife():
    Life.running = not Life.running
    if Life.running:
        Life.history.clear()
        Life.add_histroy()

def RandomLife():
    Life.rndinit()
    Life.running = True


def ClearLife():
    Life.running = False
    Life.history = []
    Life.items = [[0] * 38 for _ in range(38)]
    for x in range(36):
        for y in range(36):
            tv.itemconfig(rect[x][y], fill='lightgray', outline='lightgray')


def btnCommand(i):
    if i == 0:
        return StartLife
    elif i == 1:
        return BreakLife
    elif i == 2:
        return RandomLife
    elif i == 3:
        return ClearLife

def on_Click(event):
    x, y = (event.x - 40) // 20, (event.y - 40) // 20
    if not Life.running:
        if Life.items[x + 1][y + 1]:
            tv.itemconfig(rect[x][y], fill='lightgray', outline='lightgray')
        else:
            tv.itemconfig(rect[x][y], fill='blue', outline='blue')
        Life.items[x + 1][y + 1] = not Life.items[x + 1][y + 1]


def on_Close():
    if msgbox.askokcancel("Quit", "Do you want to quit?"):
        Life.running = False
        window.destroy()

if __name__ == '__main__':

    window = tk.Tk()
    X, Y = window.maxsize()
    W, H = 1024, 800
    winPos = f'{W}x{H}+{(X - W) // 2}+{(Y - H) // 2}'
    window.geometry(winPos)
    window.resizable(False, False)
    window.title('生命游戏')
    window.update()

    drawCanvas()
    Life = Lifes()
    drawLifes()

    tButton = [None] * 4
    bX, bY, dY = 835, 280, 60
    txt = ['开始', '暂停', '随机', '重置']
    for i in range(4):
        tButton[i] = tk.Button(window, text=txt[i],bg='whitesmoke',command=btnCommand(i))
        tButton[i].place(x=bX, y=bY + dY * i, width=120, height=40)

    window.protocol("WM_DELETE_WINDOW", on_Close)
    window.mainloop()



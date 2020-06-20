# main.py -- put your code here!
import time
from machine import I2C
from SH1107 import SH1107

screen = SH1107(I2C(0, I2C.MASTER, baudrate=400000))
screen.init()
screen.clearDisplay()
screen.verticalMode()
# screen.horizontalMode()
screen.contrastLevel(128)  # 0 - 255

# Arrays
frame = [0x00] * 2048
currentGame = [0] * 256
newGame = [0] * 256
# Glider
currentGame[56] = 1
currentGame[73] = 1
currentGame[87] = 1
currentGame[88] = 1
currentGame[89] = 1

# Tumbler
""" currentGame[84] = 1
currentGame[85] = 1
currentGame[86] = 1
currentGame[88] = 1
currentGame[89] = 1
currentGame[90] = 1
currentGame[100] = 1
currentGame[106] = 1
currentGame[118] = 1
currentGame[120] = 1
currentGame[133] = 1
currentGame[134] = 1
currentGame[136] = 1
currentGame[137] = 1
currentGame[148] = 1
currentGame[154] = 1 """

def renderFrame():
    c = 0
    m = 0
    pos = 0
    for x in range(len(newGame)):
        if c >= 16:
            c = 0
            m = m + 1
        for y in range(8):
            pos = m * 8 * 16 + (16 * y) + c
            if newGame[x] == 1:
                frame[pos] = 0xFF
            else:
                frame[pos] = 0x00
        c = c + 1

def getNextFrame():
    for x in range(len(currentGame)):
        newGame[x] = lifeOrDie(x)


def lifeOrDie(pos):
    n = getNeighbours(pos)
    if currentGame[pos] == 1:
        if n > 3:
            return 0
        elif n < 2:
            return 0
        else:
            return 1
    else:
        if n == 3:
            return 1
        else:
            return 0

def getNeighbours(pos):
    n = 0
    down = (pos + 16) if (pos + 16) <= 255 else (0 + (pos % 16))
    up = (pos - 16) if (pos - 16) >= 0 else 240 + pos
    left = (pos - 1) if (pos % 16) > 0 else (pos + 15)
    rigth = (pos + 1) if (pos % 16) < 15 else (pos - 15)
    upLeft = (up - 1) if (up % 16) > 0 else (up + 15)
    upRigth = (up + 1) if (up % 16) < 15 else (up - 15)
    downLeft = (down - 1) if (down % 16) > 0 else (down + 15)
    downRigth = (down + 1) if (down % 16) < 15 else (down - 15)

    if currentGame[up] == 1:
        n = n + 1
    if currentGame[down] == 1:
        n = n + 1
    if currentGame[left] == 1:
        n = n + 1
    if currentGame[rigth] == 1:
        n = n + 1
    if currentGame[upLeft] == 1:
        n = n + 1
    if currentGame[upRigth] == 1:
        n = n + 1
    if currentGame[downLeft] == 1:
        n = n + 1
    if currentGame[downRigth] == 1:
        n = n + 1
    return n
# Main Loop
while True:
    time.sleep(1)
    getNextFrame()
    renderFrame()
    currentGame = newGame.copy()
    screen.drawBitmap(frame, len(frame))
import array
import math

moves = ((-1, 0), (1, 0), (0, -1), (0, 1))
darken_by = 10

def setup():
    global x, y, points
    size(100, 100)
    pixelDensity(3)
    frameRate(120)
    background(255)
    x = width / 2
    y = height / 2

def draw():
    global x, y, darken_by

    move = moves[int(random(4))]
    x = (x + move[0]) % width
    y = (y + move[1]) % height
    si
    c = color(brightness(get(x, y)) - darken_by)
    set(x, y, color(c))
    

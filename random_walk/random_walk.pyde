#add_library('pdf')
add_library('svg')
#import array
#import math

amp = 1
steps = 50000
darken_by = 200
display = False
outfile_path = './subtract_1_1.svg' 

moves = ((-amp, 0), (amp, 0), (0, -amp), (0, amp))

def setup():
    global x, y, frame
    size(250, 250)#, SVG, outfile_path)
    blendMode(MULTIPLY)
    frameRate(256)
    #beginRecord(PDF, outfile_path)
    background(255)
    
    stroke(darken_by)
    strokeWeight(1)
    
    x = width / 2
    y = height / 2
    frame = 0

def draw():
    global x, y, frame
    
    move = moves[int(random(4))]
    x0, y0 = x, y
    
    x = (x + move[0]) % width
    y = (y + move[1]) % height
    
    if abs(x - x0) < 2 and abs(y - y0) < 2:
        line(x0, y0, x, y)
        
    frame += 1
    if frame == steps:
        save(outfile_path)
        exit()

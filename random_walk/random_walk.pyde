#add_library('pdf')
add_library('svg')
#import array
#import math

amp = 1  # size of random walk steps in pixel space
ampc = 0.05  # size of random walk steps in color space
driftc = 0 #.0001
c_init = [240, 240, 240, 15]  # initial color
c_mod = [256, 256, 256, 256]
steps = 5000000
disp_step = 2500
darken_by = 240
stroke_weight = 5
bgcolor = 255
display = False
outfile_path = './subtract_1_1.tif' 

moves = ((-amp, 0), (amp, 0), (0, -amp), (0, amp))
color_moves = ((-ampc, 0, 0), (ampc, 0, 0), 
               (0, -ampc, 0), (0, ampc, 0), 
               (0, 0, -ampc), (0, 0, ampc))
color_moves = ((-ampc + driftc, 0, 0, 0), (ampc + driftc, 0, 0, 0), 
               (0, -ampc + driftc, 0, 0), (0, ampc + driftc, 0, 0),
               #(0, 0, 0, -ampc), (0, 0, 0, ampc),
               (0, 0, -ampc + driftc, 0), (0, 0, ampc + driftc, 0))

def setup():
    global x, y, c, frame
    size(1920, 1080)#, SVG, outfile_path)
    blendMode(MULTIPLY)
    frameRate(60)
    #beginRecord(PDF, outfile_path)
    background(255)
    
    strokeWeight(stroke_weight)
    
    x = int(width * random(1))
    y = int(height * random(1))
    c = list(c_init)
    frame = 0

def draw():
    global x, y, c, frame
    
    for _ in range(disp_step):
        move_idx = int(random(len(moves)))
        move = moves[move_idx]
        x0, y0 = x, y
        
        x = (x + move[0]) % width
        y = (y + move[1]) % height
        
        color_move = color_moves[int(random(len(color_moves)))]
        c = [(c[i] + color_move[i]) % c_mod[i] for i in range(len(c))]
        
        stroke(*[int(i) for i in c])
        strokeWeight(int(random(2) + 1))
        
        if abs(x - x0) <= amp and abs(y - y0) <= amp:
            line(x0, y0, x, y)
            
        frame += 1
        
        
        if frame == steps:
            save(outfile_path)
            exit()
    #print(c)    
    #print('{} fps'.format(frameRate))

#add_library('pdf')
add_library('svg')
#import array
import math

frames = 4000
#amp = 1  # size of random walk steps in pixel space
#ampc = 0.05  # size of random walk steps in color space
driftc = 0 #.0001
#bgc = 255 # background color
c_init = [240, 240, 240, 15]  # initial color
c_mod = [256, 256, 256, 256]
#steps = 1000000
disp_step = 2500
stroke_weight = 5
display = False
outfile_path = '/mnt/store/processing/{}.tif' 

blend_modes = {"difference": DIFFERENCE, "subtract": SUBTRACT, "add": ADD, 
               "blend": BLEND, "darkest": DARKEST, "lightest": LIGHTEST, 
               "exclusion": EXCLUSION, "multiply": MULTIPLY, 
               "screen": SCREEN, "replace": REPLACE}

def radial_move(theta, r=1):
    return (r * cos(theta), r * sin(theta))

def setup():
    global x, y, c, frame
    
    #pg = createGraphics(1920, 1080, P2D)
    size(1920, 1080, P2D)#, SVG, outfile_path)
    #blendMode(DIFFERENCE)
    frameRate(60)
    #strokeWeight(stroke_weight)

    frame = 0

def draw():
    global frame
    
    blend_mode_key = blend_modes.keys()[int(random(len(blend_modes)))]
    blendMode(blend_modes[blend_mode_key])
    
    bgc = int(random(256))
    background(bgc)
    
    x = int(width * random(1))
    y = int(height * random(1))
    c = list(c_init)  
    c[-1] = int(random(25) + 1)
    stroke_weight = int(random(2) + 1)
    
    amp = [1, 2, 3, 5, 10, 15, 30][int(random(7))]
    ampc = random(1) ** 3
        
    if amp > 10:
        steps = [500, 1000, 10000, 50000][int(random(4))]
        
    elif amp > 3:
        steps = [1000, 10000, 50000, 100000, 250000][int(random(5))]
    
    elif amp > 1:
        steps = [10000, 50000, 100000, 250000, 500000][int(random(5))]
        
    else:
        steps = [250000, 500000, 1000000, 2500000][int(random(4))]
    
    #directions = 90
    directions = [3, 4, 5, 6, 12, 64, 90, 360][int(random(8))]
    if amp > 10 and directions > 6:
        directions = 6
    
    moves = [radial_move(2 * math.pi * th / directions, r=amp) for th in range(directions)]  
    
    color_moves = [((-ampc + driftc, 0, 0, 0), (ampc + driftc, 0, 0, 0)), 
                   ((0, -ampc + driftc, 0, 0), (0, ampc + driftc, 0, 0)),
                   #(0, 0, 0, -ampc), (0, 0, 0, ampc),
                   ((0, 0, -ampc + driftc, 0), (0, 0, ampc + driftc, 0))]
    
    exclude = 'None' #int(random(3))
    #del color_moves[exclude]
    color_moves = [move for group in color_moves for move in group]

    for _ in range(steps):
        move_idx = int(random(len(moves)))
        move = moves[move_idx]
        x0, y0 = x, y
        
        #amp = int(random(5) + 1)
        x1 = (x + move[0])
        y1 = (y + move[1])
        x = x1 % width
        y = y1 % height
        
        color_move = color_moves[int(random(len(color_moves)))]
        c = [(c[i] + color_move[i]) % c_mod[i] for i in range(len(c))]
        
        stroke(*[int(i) for i in c])
        strokeWeight(stroke_weight)
        
        adx, ady = abs(x - x0), abs(y - y0)
        if adx <= amp and ady <= amp:
            line(x0, y0, x, y)    
        else:
            line(x0, y0, x1, y1)
            line(x, y, x - move[0], y - move[1])

        if not _ % 100000:
            print(_)
    
    save(outfile_path.format(frame))
    
    with open('/mnt/store/processing/list.csv', 'a') as f:
        f.write(','.join([blend_mode_key, str(steps), str(directions), str(c[-1]), str(amp), str(ampc), str(stroke_weight), str(bgc), '\n']))
    frame += 1
    
    if frame == frames:
        exit()

    #print(c)    
    #print('{} fps'.format(frameRate))

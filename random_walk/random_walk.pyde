#add_library('pdf')
add_library('svg')
#import array
import math

frames = 2000
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
    global x, y, c, frame, pg
    
    size(1920, 1080, P2D)#, SVG, outfile_path)
    pg = createGraphics(1920, 1080, P2D)
    
    #blendMode(DIFFERENCE)
    frameRate(60)
    #strokeWeight(stroke_weight)

    frame = 0

def draw():
    global x, y, c, frame, pg
    
    blend_mode_key = blend_modes.keys()[int(random(len(blend_modes)))]
    blendMode(blend_modes[blend_mode_key])
    
    bgc = int(random(256))
    
    x = int(pg.width * random(1))
    y = int(pg.height * random(1))
    c = list(c_init)  
    c[-1] = int(random(25) + 1)
    stroke_weight = int(random(2) + 1)
    
    amp = [1, 2, 3, 5, 10, 15, 30][int(random(7))]
    ampc = random(1) ** 3
    
    steps = [250, 1000, 10000, 100000, 500000, 1000000, 2500000][int(random(7))]
    
    if amp < 3 and steps < 500000:
        steps = 500000
        
    if amp > 3 and steps > 100000:
        steps = 100000
    
    #moves = ((-amp, 0), (amp, 0), (0, -amp), (0, amp))
    
    #directions = 90
    directions = [3, 4, 5, 6, 12, 64, 90, 360][int(random(8))]
    
    moves = [radial_move(2 * math.pi * th / directions, r=amp) for th in range(directions)]  
    
    color_moves = [((-ampc + driftc, 0, 0, 0), (ampc + driftc, 0, 0, 0)), 
                   ((0, -ampc + driftc, 0, 0), (0, ampc + driftc, 0, 0)),
                   #(0, 0, 0, -ampc), (0, 0, 0, ampc),
                   ((0, 0, -ampc + driftc, 0), (0, 0, ampc + driftc, 0))]
    
    exclude = 'None' #int(random(3))
    #del color_moves[exclude]
    color_moves = [move for group in color_moves for move in group]
    
    pg.beginDraw()
    pg.background(bgc)
    pg.strokeWeight(stroke_weight)
    pg.endDraw()

    for _ in range(steps):
        move_idx = int(random(len(moves)))
        move = moves[move_idx]
        x0, y0 = x, y
        
        #amp = int(random(5) + 1)
        x = (x + move[0]) % pg.width
        y = (y + move[1]) % pg.height
        
        color_move = color_moves[int(random(len(color_moves)))]
        c = [(c[i] + color_move[i]) % c_mod[i] for i in range(len(c))]
    

        
        if abs(x - x0) <= amp and abs(y - y0) <= amp:
            pg.beginDraw()
            pg.stroke(*[int(i) for i in c])
            pg.line(x0, y0, x, y)
            pg.endDraw()    
        if not _ % 100000:
            print(_)

    image(pg, 0, 0)
    save(outfile_path.format(frame))      
    with open('/mnt/store/processing/list.csv', 'a') as f:
        f.write(','.join([blend_mode_key, str(steps), str(directions), str(c[-1]), str(amp), str(ampc), str(stroke_weight), str(bgc), '\n']))
    frame += 1
    
    if frame == frames:
        exit()
 
    #print('{} fps'.format(frameRate))

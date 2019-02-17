#add_library('pdf')
add_library('svg')
#import array
#import math

frames = 100
amp = 1  # size of random walk steps in pixel space
ampc = 0.05  # size of random walk steps in color space
driftc = 0 #.0001
bgc = 255 # background color
c_init = [240, 240, 240, 15]  # initial color
c_mod = [256, 256, 256, 256]
steps = 1000000
disp_step = 2500
stroke_weight = 5
bgc = 50
display = False
outfile_path = './out/m{}.tif' 


color_moves = ((-ampc, 0, 0), (ampc, 0, 0), 
               (0, -ampc, 0), (0, ampc, 0), 
               (0, 0, -ampc), (0, 0, ampc))

blend_modes = {"difference": DIFFERENCE, "subtract": SUBTRACT, "add": ADD, 
               "blend": BLEND, "darkest": DARKEST, "lightest": LIGHTEST, 
               "exclusion": EXCLUSION, "multiply": MULTIPLY, 
               "screen": SCREEN, "replace": REPLACE}

def setup():
    global x, y, c, frame
    size(1920, 1080)#, SVG, outfile_path)
    #blendMode(DIFFERENCE)
    frameRate(60)
    #beginRecord(PDF, outfile_path)
    
    strokeWeight(stroke_weight)
    

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
    
    amp = [2, 3, 5, 10, 15][int(random(5))]
    ampc = random(1) ** 3
    
    moves = ((-amp, 0), (amp, 0), (0, -amp), (0, amp))
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
        
        x = (x + move[0]) % width
        y = (y + move[1]) % height
        
        color_move = color_moves[int(random(len(color_moves)))]
        c = [(c[i] + color_move[i]) % c_mod[i] for i in range(len(c))]
        
        stroke(*[int(i) for i in c])
        strokeWeight(stroke_weight)
        
        if abs(x - x0) <= amp and abs(y - y0) <= amp:
            line(x0, y0, x, y)    
        if not _ % 100000:
            print(_)
    
    save(outfile_path.format(frame))
    
    with open('./out/list.csv', 'a') as f:
        f.write(','.join([blend_mode_key, str(amp), str(c[-1]), str(ampc), str(stroke_weight), str(bgc), '\n']))
    frame += 1
    
    if frame == frames:
        exit()

    #print(c)    
    #print('{} fps'.format(frameRate))

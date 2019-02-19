

samples = 4000  # number of 
outfile_path = './out/{}.tif' 

c_init = [240, 240, 240, 15]  # initial color
c_mod = [256, 256, 256, 256]
disp_step = 2500
stroke_weight = 5
display = False

# the choice of blend mode affects how colours combine when drawn onto the canvas
blend_modes = {"difference": DIFFERENCE, "subtract": SUBTRACT, "add": ADD, 
               "blend": BLEND, "darkest": DARKEST, "lightest": LIGHTEST, 
               "exclusion": EXCLUSION, "multiply": MULTIPLY, 
               "screen": SCREEN, "replace": REPLACE}


def polar_to_xy(theta, r=1):
    """Convert a point from polar to Cartesian coordinates."""
    return (r * cos(theta), r * sin(theta))


def random_draw(v):
    """Return a randomly-chosen element of v."""
    return v[int(random(len(v)))]


def setup():
    global sample_n
    
    size(1920, 1080, P2D) # P2D means we're using OpenGL
    
    sample_n = 0  # counter to exit after samples have been generated
    
    
def draw():
    global sample_n
    
    # this is a strange use of draw; normally it runs repeatedly for animations,
    # but here each iteration generates an entire image without animating properly
    
    ## sample some variables semi-randomly for the sake of exploration
    # keep the name of the blend more for the log
    blend_mode_key = random_sample(blend_modes.keys())
    blendMode(blend_modes[blend_mode_key])  # set the blend mode
    
    # background colour: solid, greyscale (0-255)
    bgc = int(random(256))
    background(bgc)  # this clears the canvas with the given colour
    
    # initial position and color of walk
    x = int(width * random(1))
    y = int(height * random(1))
    c = list(c_init)  
    c[-1] = int(random(25) + 1)  # line transparency (0-255, 255 is opaque; low values are better, at least for large step sizes or small number of steps)
    stroke_weight = int(random(2) + 1)  # line thickness
    strokeWeight(stroke_weight)
    
    # step sizes for the random walks
    amp = random_draw([1, 2, 3, 5, 10, 15, 30])  # in pixel space
    ampc = random(1) ** 3  # for the random walk in colour space
        
    # number of steps required some clumsy exclusions to minimize the number of garbage outputs (e.g. 2.5 million 30-pixel steps in 64 directions = hairball)
    steps = [500, 1000, 10000, 50000, 100000, 250000, 500000, 1000000, 2500000]
    if amp > 10:
        steps = random_draw(steps[:4])
    elif amp > 3:
        steps = random_draw(steps[1:6])
    elif amp > 1:
        steps = random_draw(steps[2:7])
    else:
        steps = random_draw(steps[5:])
    
    # number of directions each step can take (e.g. 4 -> move on a square grid)
    directions = [3, 4, 5, 6, 12, 64, 90, 360])
    if amp > 10 and directions > 6:
        # too many directions doesn't work well with large step sizes?
        directions = 6
    # get cartesian moves (i.e. possible steps) from angles (easier to evenly subdivide this way) and step size
    moves = [polar_to_xy(2 * PI * th / directions, r=amp) for th in range(directions)]  
    
    # define moves (possible steps) in colour space
    # note that they are defined as +/- pairs in each colour dimensions; they will be flattened in a few lines
    # commenting out lines will prevent stepping in that dimension of the colour space
    driftc = 0  # was messing with drift, this is vestigial and maybe broken
    color_moves = [((-ampc + driftc, 0, 0, 0), (ampc + driftc, 0, 0, 0)), # red
                   ((0, -ampc + driftc, 0, 0), (0, ampc + driftc, 0, 0)), # green
                   #(0, 0, 0, -ampc), (0, 0, 0, ampc),  # alpha (opacity)
                   ((0, 0, -ampc + driftc, 0), (0, 0, ampc + driftc, 0))]  # blue
    # the following was used to exclude one of the colour dimensions from each image
    # this doesn't seem to produce more interesting results
    exclude = None #int(random(len(color_moves))) 
    if exclude is not None:
        del color_moves[exclude]
    # now flatten the colour moves
    color_moves = [move for group in color_moves for move in group]  

    for _ in range(steps):
        # calculate step in pixel space
        x0, y0 = x, y
        move = random_sample(moves)
       
        x1 = (x + move[0])
        y1 = (y + move[1])
        
        # mirror the boundaries
        x = x1 % width
        y = y1 % height
        
        # sample and apply move in colour space
        color_move = random_sample(color_moves)
        c = [(c[i] + color_move[i]) % c_mod[i] for i in range(len(c))]
        stroke(*[int(i) for i in c])
        
        # apply move in pixel space
        adx, ady = abs(x - x0), abs(y - y0)
        if adx <= amp and ady <= amp:
            line(x0, y0, x, y)    
        else:
            # line goes through a mirrored boundary; draw on both sides (running over edge is not visible)
            line(x0, y0, x1, y1)
            line(x, y, x - move[0], y - move[1])

        # give a readout so the user can keep track of longer runs
        if not _ % 100000:
            print(_)
    
    # save the current image
    save(outfile_path.format(sample_n))
    
    # write metadata to the log file
    with open('/mnt/store/processing/list.csv', 'a') as f:
        f.write(','.join([blend_mode_key, str(steps), str(directions), str(c[-1]), str(amp), str(ampc), str(stroke_weight), str(bgc), '\n']))
    
    
    sample_n += 1
    if sample_n == samples:
        exit()

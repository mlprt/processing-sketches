import os
import array
from time import sleep

path = "/home/matt/dev/processing/random_walk/out/10kP2D_edges"
outpath = "/home/matt/dev/processing/random_walk/out/10kP2D_edges/adjusted"
file_ext = '.tif'

inc = 5

#os.makedirs(outpath, exist_ok=True)

for _, _, filenames in os.walk(path):
    file_list = filenames
    break

def setup():
    global idx, cidx
    size(1920, 1080, P2D)
    idx = -1
    cidx = -1
    
def draw():
    global idx, cidx 
    
    if cidx < idx:
        if cidx > -1:
            save(os.path.join(outpath, file_list[cidx]))
        cidx = idx
        if not file_ext in file_list[idx]:
            idx += 1
        else:
            background(255)
            img = loadImage(os.path.join(path, file_list[idx]))
            image(img, 0, 0)
            
    if keyPressed:
        if key == ENTER or key == RETURN:
            idx += 1
            sleep(0.25)
        elif key == CODED:
            loadPixels()
            if keyCode == UP:
                rows_i = pixels[:inc*width][:]
                pixels[:-inc*width] = pixels[inc*width:]
                pixels[-inc*width:] = rows_i
            elif keyCode == DOWN:
                rows_f = pixels[-inc*width:][:]
                pixels[inc*width:] = pixels[:-inc*width]
                pixels[:inc*width] = rows_f
            elif keyCode == LEFT:
                for i in range(height):
                    tmp = pixels[i * width:i * width + inc]
                    pixels[i * width: (i + 1) * width - inc] = pixels[i * width + inc: (i+1) * width]
                    pixels[(i + 1) * width - inc: (i+1) * width] = tmp
            elif keyCode == RIGHT:
                for i in range(height):
                    tmp = pixels[(i + 1) * width - inc: (i+1) * width]
                    pixels[i * width + inc:(i+1) * width] = pixels[i * width: (i+1) * width - inc]
                    pixels[i * width: i * width + inc] = tmp
            updatePixels()        

                
                # img_ = createImage(1920, 1080, RGB)
                # img_.loadPixels()
                # for i in range(height):
                #     for j in range(width):
                #         loc = j + i * width
                #         if j < inc:
                #             loc1 = (i + 1) * width - j - 1
                #             img_.pixels[loc1] = pixels[loc]
                #         else:
                #             loc1 = loc - inc
                #             img_.pixels[loc1] = pixels[loc]
                        
                # img_.updatePixels()
                # image(img_, 0, 0)
                        
                        
                # cols = []
                # for i in range(inc):
                #     cols.append(pixels[i::width][:])
                #     #print(len(cols[-1]))
                # for j in range(width - inc):
                #     pixels[j::width] == pixels[j+inc-1::width]
                # for i in range(inc):
                #     print(i-inc)
                #     pixels[width-inc::width] = cols[i]

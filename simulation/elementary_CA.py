import taichi as ti
import numpy as np
ti.init(arch=ti.gpu)

ruleset = [0, 0, 0, 1, 1, 1, 1, 0] # rule 30
# ruleset = [0, 1, 0, 0, 1, 0, 0, 1] # rule 73
# ruleset = [0, 1, 0, 1, 1, 0, 1, 0] # rule 90
# ruleset = [1, 0, 0, 1, 1, 0, 1, 0] # rule 154

n = 400
cell_size = 4 
img_size = n * cell_size

cell = ti.field(int, (n, n//2))
# rule = ti.field(int, (n, n))

@ti.func
def rule(type: int) -> int:
    i, ret = 0, 0
    for r in ti.static(ruleset):
        if(i == 7-type):
            ret = r
        i += 1
        
    return ret




@ti.kernel
def init():
    for i in range(n):
        if(ti.random() > 0.8):
            cell[i, n//2-1] = 1
        else:
            cell[i, n//2-1] = 0
    # cell[n//2, n//2-1] = 1


@ti.kernel
def run():
    for i, rj in cell:
        j = n//2-rj
        if(j < n//2-1 and i > 0 and i < n-1):
            sum = (cell[i-1, j+1] << 2) + (cell[i, j+1] << 1) + cell[i+1, j+1] # print(sum)
            cell[i, j] = rule(sum)

    
    # for i, j in cell:
    #     cell[i, j] = ti.static(ruleset[rule[i, j]])
    # for i in range(1, n):

    #     for j in range(n):

    #         cell[i, j] = cell[i, j]

gui = ti.GUI("Elementary Cellular Automata", (img_size, img_size//2))
# gui.fps_limit = 16

pause = False
init()
while gui.running:
    for e in gui.get_events(gui.PRESS, gui.MOTION):
        if e.key == gui.ESCAPE:
            gui.running = False
        elif e.key == gui.SPACE:
            pause = not pause
        elif e.key == 'r':
            cell.fill(0)
            init()
        elif e.key == 's':
            ti.imwrite(pixels, 'result.png')


    
    if not pause:
        run()

    pixels = 255 - ti.imresize(cell, img_size, img_size//2).astype(np.uint8) * 255
    gui.set_image(pixels)

    gui.show()

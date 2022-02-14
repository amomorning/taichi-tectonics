

import numpy as np

import taichi as ti

ti.init(arch=ti.gpu)

n = 64
cell_size = 8

img_size = n*cell_size

alive = ti.field(int, (n, n))
neighbs = ti.field(int, (n, n)) 


@ti.func
def count_neighbors(i, j):
    return (alive[i-1, j] + alive[i+1, j]+alive[i, j-1]+alive[i, j+1]+alive[i-1, j-1]+alive[i-1, j+1]+ alive[i+1, j-1] + alive[i+1, j+1])


@ti.kernel
def run():
    for i, j in alive:
        neighbs[i, j] = count_neighbors(i, j)

    for i, j in alive:
        if(alive[i, j] == 1):
            if(neighbs[i, j] == 2 or neighbs[i, j] == 3):
                alive[i, j] = 1
            else:
                alive[i, j] = 0
        else:
            if(neighbs[i, j] == 3):
                alive[i, j] = 1



@ti.kernel
def init():
    for i, j in alive:
        if(ti.random() > 0.8):
            alive[i, j] = 1
        else:
            alive[i, j] = 0

gui = ti.GUI('Game of Life', (img_size, img_size))
gui.fps_limit=15

pause = False
init()
while gui.running:
    for e in gui.get_events(gui.PRESS, gui.MOTION):
        if e.key == gui.ESCAPE:
            gui.running = False
        elif e.key == gui.SPACE:
            pause = not pause
        elif e.key == 'r':
            alive.fill(0)
    
    if not pause:
        run()

    gui.set_image(ti.imresize(alive, img_size).astype(np.uint8) * 255)
    gui.show()

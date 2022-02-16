import taichi as ti
ti.init(arch=ti.gpu)

# ruleset = [0, 0, 0, 1, 1, 1, 1, 0] # rule 30
# ruleset = [0, 1, 0, 0, 1, 0, 0, 1] # rule 73
# ruleset = [0, 1, 0, 1, 1, 0, 1, 0] # rule 90
ruleset = [1, 0, 0, 1, 1, 0, 1, 0] # rule 154

cell_size = 4
n = 300
img_size = n * cell_size

cell = ti.field(int, (n, n))
pixels = ti.Vector.field(3, dtype=float, shape=(img_size, img_size))
gui = ti.GUI("CA pixels", (img_size, img_size))


@ti.func
def rule(type: int) -> int:
    ret = 0
    for i in ti.static(range(len(ruleset))):
        if(i == 7-type):
            ret = ruleset[i]
        
    return ret



@ti.kernel
def init():
    for i in range(n):
        if(ti.random() > 0.5):
            cell[i, n] = 1
        else:
            cell[i, n] = 0
    # cell[n//2, n] = 1


@ti.kernel
def run(t: int):

    j = n-t
    for i in range(n):
        tmp = cell[(i+1)%n, j+1]  + (cell[i, j+1] << 1) + (cell[(i-1+n)%n, j+1] << 2)
        cell[i, j] = rule(tmp)
    
    # for i in range(n):
        # for i_ in range(cell_size):
        #     for j_ in range(cell_size):
        #         x = i * cell_size+i_
        #         y = j * cell_size+j_
        #         pixels[x, y] = ti.Vector([1.0, 1.0, 1.0]) * cell[i, j]

    for i, k in pixels:
        i_ = i // cell_size
        j_ = k // cell_size
        pixels[i, k] = ti.Vector([1.0, 1.0, 1.0]) *cell[i_, j_]
        
cell.fill(0)
pixels.fill(0)
init()
t = 0
while gui.running:

    for e in gui.get_events(gui.PRESS, gui.MOTION):
        if e.key == gui.ESCAPE:
            gui.running = False
        elif e.key == gui.SPACE:
            pause = not pause
        elif e.key == 'r':
            cell.fill(0)
            pixels.fill(0)
            init()
            t = 0
        elif e.key == 's':
            ti.imwrite(pixels, 'result.png')


    if(t < n):
        t += 1
        run(t)
    gui.set_image(pixels)
    gui.show()

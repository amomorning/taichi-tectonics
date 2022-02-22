# see: https://blog.csdn.net/Hewes/article/details/77113471
import taichi as ti

res = (800, 800)
ti.init(arch=ti.cpu, cpu_max_num_threads=1)

pixels = ti.Vector.field(3, dtype=float, shape=res)

gui = ti.GUI("Peter de Jong Attractor", res)


@ti.kernel
def init():

    # a, b, c, d = -2.0, -2.0, -1.2, 2.0
    a, b, c, d = -0.827, -1.637, 1.659, -0.943
    mag = 150.0
    ox, oy = 0.0, 0.5
    for _ in range(20000):
        nx = ti.sin(a * oy) - ti.cos(b * ox)
        ny = ti.sin(c * ox) - ti.cos(d * oy)


        i = ti.cast(nx*mag+res[0]/2, ti.i32)
        j = ti.cast(ny*mag+res[1]/2, ti.i32)
        
        # print(i, j)
        pixels[i, j] = ti.Vector([1.0, 1.0, 1.0])

        ox = nx
        oy = ny
        

pixels.fill(0)

init()

while gui.running:
    gui.set_image(pixels)
    gui.show()

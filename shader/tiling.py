import taichi as ti
import handy_shader_functions as hsf
ti.init(arch=ti.gpu)

n = 12
tile_size = 64
img_size = n * tile_size

pixels = ti.Vector.field(3, dtype=float, shape=(img_size, img_size))

@ti.func
def circle(pos, center, radius, blur):
    r = (pos - center).norm()
    t = 0.0
    if blur > 0.0:
        t = hsf.smoothstep(1.0, 1.0-blur, r/radius)
    return t

@ti.kernel
def render():
    for i, j in pixels:
        color = ti.Vector([0., 0., 0.])
        tile_size = 16

        for k in range(3):
            x = hsf.mod(i, tile_size)
            y = hsf.mod(j, tile_size)

            pos = ti.Vector([x, y])
            center = ti.Vector([tile_size/2, tile_size/2])
            radius = tile_size/2

            t = circle(pos, center, radius, 0.1)
            color += ti.Vector([1. ,1. ,1.]) * t
            color /= 2
            tile_size *= 2


        pixels[i, j] = color
    
gui = ti.GUI("Canvas", res=img_size)

while gui.running:
    render()
    gui.set_image(pixels)
    gui.show()

    


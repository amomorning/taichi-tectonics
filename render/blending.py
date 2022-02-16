import taichi as ti
ti.init(arch=ti.cpu)

n = 800
gui = ti.GUI("Blending", n)

pixels = ti.Vector.field(3, dtype=float, shape=(n, n))

@ti.kernel
def init():
    for i, j in pixels:
        r = i * 1.0 / (n-1)
        g = j * 1.0 / (n-1)
        b = 0.25
        pixels[i, j] = ti.Vector([r, g, b])

init()

while gui.running:
    gui.set_image(pixels)
    gui.show()

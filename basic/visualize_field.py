import taichi as ti
ti.init(arch=ti.cpu, debug=True)

x = ti.field(ti.f32, (256, 256))

@ti.kernel
def foo():
    for i, j in x:
        x[i, j] = (i+j)/512.0

foo()

gui = ti.GUI("Debug", (256, 256))
while gui.running:
    gui.set_image(x)
    gui.show()

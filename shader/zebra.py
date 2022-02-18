# see: https://www.shadertoy.com/view/sdlfRj
import taichi as ti
import handy_shader_functions as hsf
import numpy as np

ti.init(arch=ti.gpu)

res_x, res_y = 1080, 720

pixels = ti.Vector.field(3, dtype=float, shape=(res_x, res_y))


@ti.kernel
def render(t: ti.f32):
    for i, j in pixels:
        uv = ti.Vector([float(i)/res_x, float(j)/res_y]) * 7.

        tmp =  ti.Vector([0., 0., 0.])
        for k in range(70):
        # for k in range(42-6*ti.ceil(uv[1]), 65-6*uv[1]): 
            v = 9. - float(k)/6. +2.*ti.cos(uv[0] + ti.sin(float(k) / 6. + t))- uv[1]
            # print(v, hsf.smoothstep(0., 11., v))
            tmp = hsf.mix(tmp, ti.Vector([k%2, k%2, k%2]), hsf.smoothstep(0., 11./res_y, v))
        pixels[i, j] = tmp
        

gui = ti.GUI("Zebra Valley", (res_x, res_y))

pixels.fill(0)
t = 0.
while gui.running:
    t += 0.02
    render(t)
    gui.set_image(pixels)
    # print(pixels[0, 0])
    gui.show()

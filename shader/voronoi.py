# see: https://www.shadertoy.com/view/ldB3zc
import taichi as ti
import handy_shader_functions as hsf

ti.init(arch=ti.gpu)

res_x, res_y = 1080, 720

pixels = ti.Vector.field(3, dtype=float, shape=(res_x, res_y))

@ti.func
def hash1(n):
    return hsf.fract(ti.sin(n)*43758.5453)

@ti.func
def hash2(p):
    p = ti.Vector([p.dot(ti.Vector([127.1,311.7])), p.dot(ti.Vector([269.5,183.3]))])
    return hsf.fract(ti.sin(p)*43758.5453)

@ti.func
def voronoi(p, t):
    w = 0.01
    n = ti.floor(p)
    f = hsf.fract(p)

    m = ti.Vector([8., 0., 0., 0.])


    for j in range(-2, 3):
        for i in range(-2, 3):
            g = ti.Vector([float(i), float(j)])
            o = hash2(n+g)

            o = 0.5 * 0.5*ti.sin(t + 8.*o) 

            d = (g-f+o).norm()

            col = 0.5 + 0.5*ti.sin(hash1((n+g).dot(ti.Vector([7., 113.]))) *2.5 + 3.5 + ti.Vector([2.7+t, 2.2-t, 1.5]))
            h = hsf.smoothstep(0.0, 1.0, 0.5+0.5*(m[0] - d) / w)
            m[0] = hsf.mix(m[0], d, h) - h * (1.0 - h) * w/(1.0+3.0*w)
            m[1] = hsf.mix(m[1], col[0], h) - h * (1.0 - h) * w/(1.0+3.0*w)
            m[2] = hsf.mix(m[2], col[1], h) - h * (1.0 - h) * w/(1.0+3.0*w)
            m[3] = hsf.mix(m[3], col[2], h) - h * (1.0 - h) * w/(1.0+3.0*w)

    return m


@ti.kernel
def render(t: ti.f32):
    for i, j in pixels:
        p = ti.Vector([float(i)/res_y, float(j)/res_y]) * 9.

        v = voronoi(p, t)

        col = ti.sqrt(ti.Vector([v[1], v[2], v[3]]))

        # col *= 1.0 - 0.8*v[0]*hsf.step(p[1], 5.)
        # col *= hsf.mix(v[0], 1.0, hsf.step(p[1], 0.33))

        # col *= hsf.smoothstep(0.003, 0.005, ti.abs(p[1] - 0.33))
        # col *= hsf.smoothstep(0.003, 0.005, ti.abs(p[1] - 0.66))

        pixels[i, j] = col
        

gui = ti.GUI("Voronoi", (res_x, res_y))

pixels.fill(0)
t = 0.
while gui.running:
    t += 0.03
    render(t)
    gui.set_image(pixels)
    gui.show()

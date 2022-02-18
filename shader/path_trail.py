import taichi as ti
import handy_shader_functions as hsf
ti.init(arch=ti.gpu)

res = (800, 800)

offset_y = 30.0
offset = 120
eps = 1e-3
step = 3
N = 60
M = (res[0]-offset*2)//step
pts = ti.Vector.field(2, dtype=int, shape=(M+1, N))
pts.fill(0)

start_x = offset
start_y = float(offset) + 0.5 * float(res[1] - 2*offset)
change_y = 1.2

pixels = ti.Vector.field(3, dtype=float, shape=res)


@ti.func
def point(pos, center, radius, blur):
    r = (pos - center).norm()
    t = 0.0
    if blur > 0.0:
        t = hsf.smoothstep(1.0, 1.0-blur, r/radius)
    return t




@ti.kernel
def draw():


 

    for i in range(M+1):
        x = float(i) * step + start_x
        y = float(i) * change_y + start_y


        dy = offset_y
        for j in range(0, N):
            dy += ti.random() * 2.*ti.sqrt(j) + 2.
            pts[i, j] = ti.Vector([x, y-dy])
    

    for i, j in pixels:

        pixels[i, j] = ti.Vector([0.95, 0.9, 0.8])

        t = 1.
        for k in range(M+1):
            for l in range(N):
                if(pts[k, l][1] < res[1]-offset and pts[k, l][1] > offset):
                    t += point(ti.Vector([float(i), float(j)]), pts[k, l], 1.9, 0.9) * (1.0 - ti.cast(l, dtype=ti.f32) / N )
                  
        # t = hsf.clamp(t, 1.0, 2.0)
        pixels[i, j] -= ti.Vector([0.95, 0.9, 0.8])*(t-1.)



gui = ti.GUI("Path trail", res)


draw()

W, H = res
while gui.running:
    gui.set_image(pixels)
    gui.line([offset/W, offset/H], [offset/W, 1-offset/H], 1.2, 0x0)
    gui.line([offset/W, offset/H], [1-offset/W, offset/H], 1.2, 0x0)
    gui.line([offset/W, 1-offset/H], [1-offset/W, 1-offset/H], 1.2, 0x0)
    gui.line([1-offset/W, 1-offset/H], [1-offset/W, offset/H], 1.2, 0x0)
    # print(start_x, start_y, change_y, M*step)
    gui.line([start_x/W, start_y/H], [(start_x + M*step)/W, (start_y+M*change_y)/H], 1.3, 0x0)
    gui.line([start_x/W, (start_y-offset_y)/H], [(start_x + M*step)/W, (start_y+M*change_y-offset_y)/H], 1.3, 0x0)
    gui.show()

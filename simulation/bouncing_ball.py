import taichi as ti
from random import randint
ti.init(arch=ti.gpu)

N = 500
w, h = 1600, 800
pixels = ti.Vector.field(3, dtype=float, shape=(w, h))


@ti.data_oriented
class Ball:
    def __init__(self, N):
        self.N = N
        self.radius = ti.field(dtype=float, shape=N)
        self.pos = ti.Vector.field(2, dtype=float, shape=N)
        self.v = ti.Vector.field(2, dtype=float, shape=N)
        self.color=ti.field(dtype=int, shape=N)
    
    @ti.kernel
    def initialize(self, i:int, x:int, y:int, radius:float):
        self.radius[i] = radius
        self.pos[i] = ti.Vector([x, y])
        self.v[i] = ti.Vector([ti.random(dtype=float), ti.random(dtype=float)])-0.5
        self.v[i] /= self.v[i].norm()
        self.color[i] = 0xffffff
        

    @ti.func
    def update(self, rate: ti.f32):

        for i in range(self.N):
            self.pos[i] += self.v[i] * rate
            self.color[i] = 0xffffff

            if(self.pos[i][0] > w or self.pos[i][0] < 0):
                self.v[i][0] = - self.v[i][0]

            if(self.pos[i][1] > h or self.pos[i][1] < 0):
                self.v[i][1] = - self.v[i][1]

        for i in range(self.N):

            for j in range(i):
                if((self.pos[i] - self.pos[j]).norm() < self.radius[i] + self.radius[j]):
                    # dv = (self.pos[j] - self.pos[i]) / (self.pos[j] - self.pos[i]).norm()
                    t = self.v[i]
                    self.v[i] = self.v[j]
                    self.v[j] = t
                    self.color[i] = 0x000000
                    self.color[j] = 0x000000
                    # self.v[i] /= self.v[i].norm()
                    break
                
                # if((self.pos[i] - self.pos[j]).norm() < self.radius[i] + self.radius[j] + 1):
                #     flag = True
                #     t = self.v[i] 
                #     self.v[i] = self.v[j] 
                #     self.v[j] = t
                #     self.color[i] = 0xff0000
                #     self.color[j] = 0xff0000
                #     break




gui = ti.GUI("Bouncing Ball", res=(w , h))

balls = Ball(N)

for i in range(N):
    balls.initialize(i, randint(10, w-10), randint(10, h-10), randint(2, 10))
    # print(balls.getBall(i))
@ti.func
def clamp(v, v_min, v_max):
    return ti.min(ti.max(v, v_min), v_max)

@ti.func
def smoothstep(edge1, edge2, v):
    assert(edge1 != edge2)
    t = (v-edge1) / float(edge2-edge1)
    t = clamp(t, 0.0, 1.0)

    return (3-2 * t) * t**2


@ti.func
def circle(pos, center, radius):
    dist = (pos - center).norm()
    ret = 0.0
    ret = smoothstep(1.0, 0.8, dist/radius)
    return ret


@ti.kernel
def draw():
    balls.update(2)
    alpha = 0.1
    for i, j in pixels:
        c = ti.Vector([0.0, 0.0, 0.0])*alpha + pixels[i, j] *(1-alpha) 
        for k in range(N):
            pos = balls.pos[k]
            t = circle(pos, ti.Vector([i, j]), balls.radius[k])
            c += ti.Vector(ti.hex_to_rgb(balls.color[k])) * t

        pixels[i, j] = c*0.8


while gui.running:
    for e in gui.get_events(gui.PRESS, gui.MOTION):
        if e.key == 's':
            ti.imwrite(pixels, 'result.png')

    draw()
    gui.set_image(pixels)
    gui.show()


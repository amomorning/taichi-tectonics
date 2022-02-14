import taichi as ti
from random import randint
ti.init(arch=ti.gpu)

bg = ti.field(dtype=int, shape=2)
bg[0], bg[1] = 1600, 800
N = 30

def dist(a, b):
    return ti.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

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
        

    @ti.kernel
    def update(self, rate: ti.f32):

        for i in range(self.N):
            self.pos[i] += self.v[i] * rate
            self.color[i] = 0xffffff

            if(self.pos[i][0] > bg[0] or self.pos[i][0] < 0):
                self.v[i][0] = - self.v[i][0]

            if(self.pos[i][1] > bg[1] or self.pos[i][1] < 0):
                self.v[i][1] = - self.v[i][1]

        for i in range(self.N):

            for j in range(i):
                if((self.pos[i] - self.pos[j]).norm() < self.radius[i] + self.radius[j]):
                    # dv = (self.pos[j] - self.pos[i]) / (self.pos[j] - self.pos[i]).norm()
                    t = self.v[i]
                    self.v[i] = self.v[j]
                    self.v[j] = t
                    self.color[i] = 0x222222
                    self.color[j] = 0x222222
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


    def getBall(self, i: int):
        return self.pos[i][0], self.pos[i][1], self.radius[i], self.color[i]

        


gui = ti.GUI("Bouncing Ball", res=(bg[0] , bg[1]))

balls = Ball(N)

for i in range(N):
    balls.initialize(i, randint(10, bg[0]-10), randint(10, bg[1]-10), randint(2, 10))
    # print(balls.getBall(i))



def draw():
    balls.update(2)
    for i in range(N):
        x, y, r, c = balls.getBall(i)
        gui.circle((x/bg[0], y/bg[1]), radius=r, color=c)

while gui.running:
    draw()
    gui.show()


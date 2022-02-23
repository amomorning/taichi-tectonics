import taichi as ti
ti.init(arch=ti.cpu)


curser_radius = 1.0/32
picking = ti.field(ti.i32, 1)
curser = ti.Vector.field(2, ti.f32, 1)
res = (800, 800)

substepping = 10
k = 2.5
h = 16.7e-3
dh = h/substepping

def ordered(a, b): 
    if(a < b): return (a, b)
    else: return (b, a)

# read file
with open('elasticity/ditto.txt', 'r') as f:
    N, m = map(int, f.readline().split())
    vs = ti.Vector.field(2, ti.f32, N)
    fs = ti.Vector.field(2, ti.f32, N)

    for i in range(N):
        x, y, z = map(float, f.readline().split())
        vs[i] = (ti.Vector([x, y])+55)/120
    lst = []
    for i in range(m):
        a, b, c = map(int, f.readline().split())

        t = ordered(a, b)
        if not t in lst:
            lst.append(t)
        t = ordered(c, b)
        if not t in lst:
            lst.append(t)
        t = ordered(a, c)
        if not t in lst:
            lst.append(t)

    M = len(lst)
    es = ti.Vector.field(2, ti.i32, M)
    lr = ti.field(ti.f32, M)
    for i in range(M):
        u, v = lst[i]
        es[i] = ti.Vector([u, v])
        lr[i] = (vs[u] - vs[v]).norm()



@ti.kernel
def compute_gradient():
    for i in fs:
        fs[i] = ti.Vector([0, 0])

    for i in range(M):
        u, v = es[i][0], es[i][1]
        l = (vs[u] - vs[v]).norm()
        fs[v] += (vs[u]-vs[v])*k*(l - lr[i])/lr[i]
        fs[u] += -fs[v]
        
        

@ti.kernel
def update():

    for i in range(N):
        vs[i] += dh*fs[i]

    if picking[0]:
        for i in range(N):
            r = vs[i] - curser[0]
            if(r.norm() < curser_radius):
                vs[i] = curser[0]
                pass




paused = False
gui = ti.GUI("Ditto", res)

while gui.running:
    picking[0] = 0
    # key events
    for e in gui.get_events(ti.GUI.PRESS):
        if e.key in [ti.GUI.ESCAPE, ti.GUI.EXIT]:
            exit()
        

    if gui.is_pressed(ti.GUI.LMB):
        curser[0] = gui.get_cursor_pos()
        picking[0] = 1



    if not paused:
        for i in range(substepping):
            compute_gradient()
            update()

    # render
    pos = vs.to_numpy()
    for i in range(M):
        a = (pos[es[i][0]][0], pos[es[i][0]][1])
        b = (pos[es[i][1]][0], pos[es[i][1]][1])
        gui.line(a, b, radius=1., color=0xffffff)

    for i in range(N):
        gui.circle((vs[i][0], vs[i][1]), radius=curser_radius*100, color=0xffffff)

    if picking[0]: 
        gui.circle((curser[0][0], curser[0][1]), radius=curser_radius*300, color=0xFF8888)
    gui.show()

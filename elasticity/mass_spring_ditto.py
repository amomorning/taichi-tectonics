import taichi as ti
ti.init(arch=ti.cpu)


curser_radius = 1.0/32
picking = ti.field(ti.i32, 1)
curser = ti.Vector.field(2, ti.f32, 1)
res = (800, 800)

substepping = 100
k = 10.
h = 16.7e-3
dh = h/substepping
mass = 1.0

using_auto_diff = True
damping_toggle = ti.field(ti.i32, 1)
damping_toggle[0] = 1
total_energy = ti.field(ti.f32, (), needs_grad=True)

def ordered(a, b): 
    if(a < b): return (a, b)
    else: return (b, a)

# read file
with open('elasticity/ditto.txt', 'r') as f:
    N, m = map(int, f.readline().split())
    vs = ti.Vector.field(2, ti.f32, N, needs_grad=True)
    ve = ti.Vector.field(2, ti.f32, N)
    fs = ti.Vector.field(2, ti.f32, N)

    for i in range(N):
        x, y, z = map(float, f.readline().split())
        vs[i] = (ti.Vector([x, y])+55)/120
        ve[i] = ti.Vector([0., 0.])
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
    l0 = ti.field(ti.f32, M)
    for i in range(M):
        u, v = lst[i]
        es[i] = ti.Vector([u, v])
        l0[i] = (vs[u] - vs[v]).norm()



@ti.kernel
def compute_gradient():
    for i in fs:
        fs[i] = ti.Vector([0, 0])

    for i in range(M):
        u, v = es[i][0], es[i][1]
        l = (vs[u] - vs[v]).norm()
        fs[v] += -(vs[u]-vs[v])*k*(l - l0[i])/l0[i]
        fs[u] += -(vs[v]-vs[u])*k*(l - l0[i])/l0[i]
        

@ti.kernel
def compute_total_energy():
    for i in range(M):
        u, v = es[i][0], es[i][1]
        l = (vs[u] - vs[v]).norm()
        total_energy[None] += 0.5 * k * (l-l0[i]) * (l-l0[i])
        

@ti.kernel
def update():

    # explicit
    for i in range(N):

        if using_auto_diff:
            ve[i] -= dh*vs.grad[i] / mass
        else:
            ve[i] -= dh*fs[i] / mass

        ve[i] *= ti.exp(-dh*damping_toggle[0])
        vs[i] += dh * ve[i]


    if picking[0]:
        for i in range(N):
            r = vs[i] - curser[0]
            if(r.norm() < curser_radius):
                vs[i] = curser[0]
                ve[i] = ti.Vector([0.0, 0.0])
                pass




paused = False
gui = ti.GUI("Ditto", res)

while gui.running:
    picking[0] = 0
    # key events
    for e in gui.get_events(ti.GUI.PRESS):
        if e.key in [ti.GUI.ESCAPE, ti.GUI.EXIT]:
            exit()
        elif e.key == ti.GUI.SPACE:
            paused = not paused
        elif e.key =='d' or e.key == 'D':
            damping_toggle[0] = not damping_toggle[0]

    if gui.is_pressed(ti.GUI.LMB):
        curser[0] = gui.get_cursor_pos()
        picking[0] = 1



    if not paused:
        for i in range(substepping):
            if using_auto_diff:
                total_energy[None]=0
                with(ti.Tape(total_energy)):
                    compute_total_energy()
            else:
                compute_gradient()
            update()

    # render
    pos = vs.to_numpy()
    for i in range(M):
        a = (pos[es[i][0]][0], pos[es[i][0]][1])
        b = (pos[es[i][1]][0], pos[es[i][1]][1])
        gui.line(a, b, radius=1., color=0xffffff)

    for i in range(N):
        color = 0xffffff
        # if i == 0: color=0xffffff
        gui.circle((vs[i][0], vs[i][1]), radius=curser_radius*100, color=color)
        # gui.text("(%.2f, %.2f)"%(ve[i][0]*1000., ve[i][1]*1000.), (vs[i][0], vs[i][1]), color=0xffff00)

    if picking[0]: 
        gui.circle((curser[0][0], curser[0][1]), radius=curser_radius*300, color=0xFF8888)
    gui.show()

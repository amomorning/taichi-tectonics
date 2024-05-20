import taichi as ti
ti.init(arch=ti.cpu)

res = (800, 800)
picking = ti.field(ti.i32, 1)
curser = ti.Vector.field(2, ti.f32, 1)
curser_radius = 1.0/32


substepping = 50
m = 1.
h = 16.7e-3
dh = h/substepping

N, N_triangles = 16, 16
vertices = ti.Vector.field(2, ti.f32, N)
faces = ti.Vector.field(3, ti.i32, N_triangles)

# read file
with open('elasticity/ditto.txt', 'r') as f:
    f.readline()
    # N, M = map(int, f.readline().split())

    for i in range(N):
        a, b, c= map(float, f.readline().split())
        vertices[i] = (ti.Vector([a, b])+55)/120
        
    for i in range(N_triangles):
        a, b, c = map(int, f.readline().split())
        faces[i] = ti.Vector([a, b, c])


using_auto_diff = False
damping_toggle = ti.field(ti.i32, 1)

x = ti.Vector.field(2, ti.f32, N, needs_grad=True)
v = ti.Vector.field(2, ti.f32, N)
elements_Dm_inv = ti.Matrix.field(2, 2, ti.f32, N_triangles)
elements_V0 = ti.field(ti.f32, N_triangles)

total_energy = ti.field(ti.f32, (), needs_grad=True)

YoungsModulus = ti.field(ti.i32, ())
PoissonsRatio = ti.field(ti.f32, ())
LameMu = ti.field(ti.f32, ())
LameLa = ti.field(ti.f32, ())

@ti.kernel
def initialize():
    YoungsModulus[None] = 1e3
    for i in range(N):
        x[i] = vertices[i]
        v[i] = ti.Vector([0.0, 0.0])
    
    for i in range(N_triangles):
        Dm = compute_D(i)
        elements_Dm_inv[i] = Dm.inverse()
        elements_V0[i] = ti.abs(Dm.determinant())/2


@ti.func
def clamp(v, v_min, v_max):
    return ti.min(ti.max(v, v_min), v_max)

    
@ti.func
def compute_D(i):
    # print(i)
    a = faces[i][0]
    b = faces[i][1]
    c = faces[i][2]
    return ti.Matrix.cols([x[b] - x[a], x[c] - x[a]])

@ti.func
def compute_R_2D(F):
    R, S = ti.polar_decompose(F, ti.f32)
    return R

@ti.kernel
def updateLameCoeff():
    E = YoungsModulus[None]
    nu = PoissonsRatio[None]
    LameLa[None] = E*nu / ((1+nu)*(1-2*nu))
    LameMu[None] = E / (2*(1+nu))

@ti.kernel
def compute_total_energy():
    for i in range(N_triangles):
        Ds = compute_D(i)
        F = Ds @ elements_Dm_inv[i]
        # co-rotated linear elasticity
        R = compute_R_2D(F)
        Eye = ti.Matrix.cols([[1.0, 0.0], [0.0, 1.0]])
        element_energy_density = LameMu[None]*((F-R)@(F-R).transpose()).trace() + 0.5*LameLa[None]*(R.transpose()@F-Eye).trace()**2

        total_energy[None] += element_energy_density * elements_V0[i]   


@ti.kernel
def update():
    for i in range(1, N):
        acc = -x.grad[i]/m
        v[i] += dh*acc
        
        x[i] += dh*v[i]
    
    for i in v:
        if damping_toggle[0]:
            v[i] *= ti.exp(-dh*5)


    if picking[0]:
        for i in range(N):
            r = x[i] - curser[0]
            if(r.norm() < curser_radius):
                x[i] = curser[0]
                v[i] = ti.Vector([0.0, 0.0])
                pass

    for i in range(N):
        if x[i][0] > 1.0 or x[i][0] < 0.0:
            clamp(0.0, 1.0, x[i][0])
            v[i][0] = 0
        if x[i][1] > 1.0 or x[i][1] < 0.0:
            clamp(0.0, 1.0, x[i][1])
            v[i][1] = 0



paused = False
gui = ti.GUI("Ditto", res)


initialize()
updateLameCoeff()


while gui.running:
    picking[0] = 0

    
    for e in gui.get_events(ti.GUI.PRESS):
        if e.key in [ti.GUI.ESCAPE, ti.GUI.EXIT]:
            exit()
        elif e.key == ti.GUI.SPACE:
            paused = not paused
        elif e.key =='d' or e.key == 'D':
            damping_toggle[0] = not damping_toggle[0]
        elif e.key =='r' or e.key == 'R':
            initialize()
        updateLameCoeff()

    if gui.is_pressed(ti.GUI.LMB):
        curser[0] = gui.get_cursor_pos()
        picking[0] = 1

    if not paused:
        for i in range(substepping):
            total_energy[None]=0
            with(ti.Tape(total_energy)):
                compute_total_energy()
            update()

    pos = x.to_numpy()

    for i in range(N_triangles):
        a = (pos[faces[i][0]][0], pos[faces[i][0]][1])
        b = (pos[faces[i][1]][0], pos[faces[i][1]][1])
        c = (pos[faces[i][2]][0], pos[faces[i][2]][1])

        gui.triangle(a, b, c, color=0xf0bbe6)
        gui.line(a, b, radius=1., color=0xff0000)
        gui.line(a, c, radius=1., color=0xff0000)
        gui.line(b, c, radius=1., color=0xff0000)

    for i in range(N):
        color = 0x4577cc
        # if i == 0: color=0xffffff
        gui.circle((pos[i][0], pos[i][1]), radius=curser_radius*100, color=color)

    if picking[0]: 
        gui.circle((curser[0][0], curser[0][1]), radius=curser_radius*300, color=0xFF8888)

    gui.text("Space: pause", (0.1, 0.96), color=0xffffff)
    gui.text("R: Initialize", (0.1, 0.93), color=0xffffff)
    if(damping_toggle[0]):
        gui.text("D: Damping On", (0.1, 0.9), color=0xffffff)
    else:
        gui.text("D: Damping Off", (0.1, 0.9), color=0xffffff)
    
    gui.show()

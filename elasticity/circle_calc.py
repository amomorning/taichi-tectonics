import taichi as ti
ti.init(ti.gpu)

res = (800, 800)
pixels = ti.Vector.field(3, ti.f32, res)

force = ti.Vector.field(2, ti.f32, 1)
pos = ti.Vector.field(2, ti.f32, 1)
vel = ti.Vector.field(2, ti.f32, 1)
mass = ti.field(ti.f32, 1)
mass[0] = 1.0


pos[0] = ti.Vector([0.05, 0.05])
vel[0] = ti.Vector([0.05, -0.05])

@ti.kernel
def explicit_update(h: ti.f32):
    force[0] = -pos[0]
    pos[0] += vel[0] * h
    vel[0] += force[0]/mass[0] * h


@ti.kernel
def simplicit_update(h: ti.f32):
    force[0] = -pos[0]
    vel[0] += force[0]/mass[0] * h
    pos[0] += vel[0] * h

@ti.kernel
def implicit_update(h: ti.f32):
    I = ti.Matrix([[1.0, 0.0], [0.0, 1.0]])

    x = pos[0]
    t0 = x.norm()
    # Baraff and Witkin, 1998
    K = ((x/t0) @ force[0].transpose()) 

    A = I - h**2/mass[0]*K

    force[0] = -pos[0]
    vel[0] = A.inverse() @ (vel[0] + force[0]/mass[0] * h)
    pos[0] += vel[0] * h


gui = ti.GUI("Circle", res)



@ti.func
def smoothstep(edge1, edge2, v):
    assert(edge1 != edge2)
    t = (v-edge1) / float(edge2-edge1)
    t = clamp(t, 0.0, 1.0)

    return (3-2 * t) * t**2

@ti.func
def clamp(v, v_min, v_max):
    return ti.min(ti.max(v, v_min), v_max)

@ti.kernel
def circle(x:ti.f32, y:ti.f32, radius:ti.f32):
    v = ti.Vector([x*res[0], y*res[1]])
    for i, j in pixels:
        u = ti.Vector([i, j])
        r = (u-v).norm()
        t = smoothstep(1.0, 1.0-0.6, r/radius)
        pixels[i, j] += ti.Vector([1., 1., 1.]) * t
        


for i in range(10000):
    # explicit_update(0.05)
    # simplicit_update(0.05)
    implicit_update(0.05)
    circle(pos[0][0]+0.5, pos[0][1]+0.5, 0.9)
    gui.set_image(pixels)
    gui.show()

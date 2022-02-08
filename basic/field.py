import taichi as ti
ti.init(arch=ti.cpu)

# 2d pixels
pixels = ti.field(dtype=float, shape=(16, 8))
pixels[1, 2] = 42

# vector field
vf = ti.Vector.field(3, ti.f32, shape=4)
@ti.kernel
def foo():
    v = ti.Vector([1, 2, 3])
    vf[0] = v
    print(vf[1])        # [0.000000, 0.000000, 0.000000]

foo()

# scalar: must use [None]
zero_d = ti.field(dtype=float, shape=())
zero_d[None] = 1.5
print(zero_d[None])     # 1.5

zero_d_vec = ti.Vector.field(3, ti.f32, shape=())
zero_d_vec[None] = ti.Vector([1, 2, 3])
print(zero_d_vec[None]) # [1. 2. 3.]

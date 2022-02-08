import taichi as ti
ti.init(arch=ti.cpu)

vec3f = ti.types.vector(3, ti.f32)
mat2f = ti.types.matrix(2, 2, ti.f32)
ray = ti.types.struct(ro=vec3f, rd=vec3f, l=ti.f32)

@ti.kernel
def foo():
    a = vec3f(0.0) 
    print(a)                # [0.000000, 0.000000, 0.000000]
    d = vec3f(0, 1, 0)
    print(d)                # [0.000000, 1.000000, 0.000000]

    B = mat2f([[1.5, 1.4], [1.3, 1.2]])
    print("B =", B)         # B = [[1.500000, 1.400000], [1.300000, 1.200000]]

    r = ray(ro=a, rd=d, l=1)
    # r = ray(a, d, 1) UnboundLocalError: local variable 'entries' referenced before assignment
    #print(r) Error: Cannot initialize scalar expression
    print("r.ro =", r.ro)   # r.ro = [0.000000, 0.000000, 0.000000]
    print("r.rd =", r.rd)   # r.rd = [0.000000, 1.000000, 0.000000]

foo()


@ti.kernel
def bar():
    a = ti.Vector([0.0, 0.0, 0.0])
    print(a)                # [0.000000, 0.000000, 0.000000]
    print(a[0])             # 0.000000
    d = ti.Vector([0.0, 1.0, 0.0])
    print(d)                # [0.000000, 1.000000, 0.000000]
    B = ti.Matrix([[1.5, 1.4], [1.3, 1.2]])
    print(B)                # [[1.500000, 1.400000], [1.300000, 1.200000]]
    print(B[1, 1])          # 1.200000

    r = ti.Struct(ro=a, rd=d, l=1)
    print("r.ro =", r.ro)   # r.ro = [0.000000, 0.000000, 0.000000] 
    print("r.rd =", r.rd)   # r.rd = [0.000000, 1.000000, 0.000000]

bar()

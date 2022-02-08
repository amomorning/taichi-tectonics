import taichi as ti
ti.init(arch=ti.cpu)


def foo():
    print("this is normal")
    a = 1
    a = 2.7
    print(a)

foo()
# this is normal
# 2.7
    
@ti.kernel
def bar():
    print("this is taichi")
    a = 1
    a = 2.7
    print(a)

bar()
# this is taichi
# 2


@ti.kernel
def zot():
    a = 1.7
    b = ti.cast(a, ti.i32)
    c = ti.cast(b, ti.f32)
    print("b =", b) # b = 1
    print("c =", c) # c = 1.000000

zot()

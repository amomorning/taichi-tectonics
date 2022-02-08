import taichi as ti
ti.init(arch=ti.cuda)

@ti.kernel
def ker():
    for i in range(40):
        print(i)

ker()

@ti.kernel
def my_ker():
    print('inside kernel')

print('before kernel')
my_ker()
print('after kernel')
ti.sync()
print('after sync')

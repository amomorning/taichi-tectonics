import taichi as ti
ti.init(arch=ti.cpu, cpu_max_num_threads=8)

x = ti.field(ti.i32)
ti.root.dense(ti.i, 4).dense(ti.i, 4).place(x)

@ti.kernel
def print_id():
    for i in x:
        print(i, end = " ")
print_id()

# first output
# 0 1 2 3 8 9 10 11 4 5 6 7 12 13 14 15
# second output
# 8 9 10 11 0 1 2 3 12 13 14 15 4 5 6 7 
# third output
# 0 1 2 3 4 5 6 7 12 13 14 15 8 9 10 11

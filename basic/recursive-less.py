import taichi as ti
ti.init(arch=ti.cpu, cpu_max_num_threads=1)

# 尾递归：计算集中在递归过程末尾
def fact(n):
    if n == 1: 
        return 1
    return n * fact(n-1)
    
# 用循环模拟尾递归
@ti.kernel
def ti_fact(n:ti.int32) -> ti.int64:
    tot = 1
    tmp = n
    while True:
        if(tmp == 1): 
            break
        tot *= tmp
        tmp = tmp - 1
    return tot


print(fact(5))
print(ti_fact(5))


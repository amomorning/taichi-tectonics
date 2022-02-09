import taichi as ti
ti.init(arch=ti.cpu)

n = 4
# step 1: create sparse matrix builder
K = ti.linalg.SparseMatrixBuilder(n, n, max_num_triplets=100)

@ti.kernel
def fill(A: ti.linalg.sparse_matrix_builder()):
    for i in range(n):
        A[i, i] += i

# step 2: fill the number
fill(K)

print(">>>> K.print")
K.print_triplets()
# n=4, m=4, num_triplets=4 (max=100)
# (0, 0) val=0.0
# (1, 1) val=1.0
# (2, 2) val=2.0
# (3, 3) val=3.0

# step 3: create a sparse matrix
A = K.build()
print(">>>> A.print")
print(A)
# [0, 0, 0, 0]
# [0, 1, 0, 0]
# [0, 0, 2, 0]
# [0, 0, 0, 3]

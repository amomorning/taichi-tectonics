import taichi as ti
ti.init(arch=ti.gpu)

n = 4
# step 1: create sparse matrix builder
K = ti.SparseMatrixBuilder(n, n, max_num_triplets=100)

@ti.kernel
def fill(A: ti.sparse_matrix_builder()):
    for i in range(n):
        A[i, i] += i

# step 2: fill the number
fill(K)

print(">>>> K.print")
K.print_triplets()

# step 3: create a sparse matrix

A = K.build()
print(">>>> A.print")
print(A)

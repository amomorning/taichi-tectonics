import taichi as ti
import numpy as np

ti.init(arch=ti.cpu)

N = 100
begins = np.random.random((N, 2))
directions = np.random.uniform(low=-0.05, high=0.05, size=(N, 2))
directions /= np.linalg.norm(directions, axis=1).reshape(-1, 1) * 30

def update():
    global begins, directions
    for i in range(N):
        for j in range(2):
            if begins[i][j] < 0:
                begins[i][j] = 1+begins[i][j]
            if begins[i][j] > 1:
                begins[i][j] = begins[i][j]-1
    
    for i in range(N):
        dir = np.zeros(2)
        num = 0
        alpha=0.9
        for j in range(N):
            if i == j:
                continue
            diff = begins[i] - begins[j]
            dist = np.linalg.norm(diff)
            if dist < 0.02:
                directions[i] = alpha * directions[i] + (1-alpha) * (-directions[j])
            elif dist < 0.1:
                dir += directions[j]
                num += 1
        if num > 0:
            directions[i] = alpha * directions[i] + (1-alpha) * dir / num

        directions[i] /= np.linalg.norm(directions[i]) * 30
    
    begins += directions * 0.2

# vm = ti.tools.VideoManager('./results', framerate=24, automatic_build=True)
gui = ti.GUI('arrows', res=(800, 800))
while gui.running:
    update()
    gui.arrows(orig=begins, direction=directions, radius=1)
    # vm.write_frame( gui.get_image())
    gui.show()

# vm.make_video()

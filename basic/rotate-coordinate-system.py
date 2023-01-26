import taichi as ti
import numpy as np

arch = ti.vulkan if ti._lib.core.with_vulkan() else ti.cuda
ti.init(arch=arch, debug=True)


# draw coordinate system
class CoordinateSystem:

    def __init__(self, length = 1):
        self.axes = [ti.Vector.field(3, dtype=ti.f32, shape = 2) for _ in range(3)]
        self.color = [None for _ in range(3)]
        for i in range(3):
            self.axes[i][1] = [length if j == i else 0 for j in range(3)]
            self.color[i] = tuple([1 if j==i else 0 for j in range(3)])
    
    def draw(self, scene):
        for i in range(3):
            scene.lines(self.axes[i], color=self.color[i], width = 5.0)


@ti.func
def rotateX(points, theta):
    sin = ti.sin(theta)
    cos = ti.cos(theta)
    Rx = ti.Matrix([[1, 0, 0], [0, cos, -sin], [0, sin, cos]])
    return Rx @ points

@ti.func
def rotateY(points, theta):
    sin = ti.sin(theta)
    cos = ti.cos(theta)
    Ry = ti.Matrix([[cos, 0, sin], [0, 1, 0], [-sin, 0, cos]])
    return Ry @ points

@ti.func
def rotateZ(points, theta):
    sin = ti.sin(theta)
    cos = ti.cos(theta)
    Rz = ti.Matrix([[cos, -sin, 0], [sin, cos, 0], [0, 0, 1]])
    return Rz @ points
    
N = 3
point_coord = ti.Vector.field(3, dtype=ti.f32, shape=N+1)
line_coord = ti.Vector.field(3, dtype=ti.f32, shape=N*2)

@ti.kernel
def reset():
    point_pos = ti.Matrix.zero(ti.f32, 3, 3)
    for i in ti.static(range(3)):
        point_pos[i, i] = 1 
    
    theta = ti.random(ti.f32) * 2
    point_pos = rotateX(point_pos, theta)
    print(theta)
    
    theta = ti.random(ti.f32) * 2
    point_pos = rotateY(point_pos, theta)
    print(theta)

    theta = ti.random(ti.f32) * 2
    point_pos = rotateZ(point_pos, theta)
    print(theta)

    for i in ti.static(range(3)):
        line_coord[i*2] = point_pos @ ti.Matrix.unit(3, i)
        point_coord[i] = point_pos @ ti.Matrix.unit(3, i)


def set_gui(window):
    gui = window.get_gui()
    with gui.sub_window('Controller', 0, 0, .2, .2):
        gui.text('Press \'r\' or click')
        is_clicked = gui.button('rotate')
        if is_clicked:
            reset()

def main():

    window = ti.ui.Window("Test for rotating coordinate system", (768, 768), vsync=True)
    canvas = window.get_canvas()
    scene = ti.ui.Scene()
    camera = ti.ui.Camera()
    camera.position(1, 2, 3)
    camera.lookat(0, 0, 0)
    cs = CoordinateSystem(100)


    set_gui(window)
    reset()

    while window.running:
        camera.track_user_inputs(window, movement_speed=0.03, yaw_speed=0.03, pitch_speed=0.5, hold_key=ti.ui.RMB)
        if window.get_event(ti.ui.PRESS):
            if window.event.key == 'r':
                reset()

        cs.draw(scene)
        scene.set_camera(camera)
        set_gui(window)
        scene.ambient_light((0.8, 0.8, 0.8))
        scene.point_light(pos=(0.5, 1.5, 1.5), color=(1, 1, 1))

        scene.particles(point_coord, color = (0.68, 0.26, 0.19), radius = 0.1)
        scene.lines(line_coord, color = (0.28, 0.68, 0.99), width = 5.0)
        
        canvas.scene(scene)
        window.show()

if __name__ == '__main__':
    main()

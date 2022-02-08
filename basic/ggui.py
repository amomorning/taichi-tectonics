import taichi as ti
ti.init(arch=ti.gpu)

window = ti.ui.Window('Window Title', (800, 600))

scene = ti.ui.Scene()
canvas = window.get_canvas()

camera = ti.ui.make_camera()
camera.position(0.5, 1.0, 1.95)
camera.lookat(0.5, 0.3, 0.5)
camera.fov(55)

vertices = ti.Vector.field(3, ti.f32, shape=1)
vertices[0] = ti.Vector([0.0, 0.0, 0.0])

colors = ti.Vector.field(4, ti.f32, shape=1)
colors[0] = ti.Vector([1.0, 1.0, 1.0, 1.0])

def render():
    # hold left mouse button (LMB) to move
    camera.track_user_inputs(window, movement_speed=0.03, hold_key=ti.ui.LMB) 
    
    scene.set_camera(camera)
    scene.ambient_light((0.1, 0.1, 0.1))
    
    scene.particles(vertices, per_vertex_color=colors, radius=0.1)
    scene.point_light(pos=(0.5, 1.5, 0.5), color=(0.5, 0.5, 0.5))
    scene.point_light(pos=(0.5, 1.5, 1.5), color=(0.5, 0.5, 0.5))

    canvas.scene(scene)


while window.running:
    render()
    window.show()

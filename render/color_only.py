import taichi as ti
import numpy as np
from render_util import Hittable_list, Sphere, Camera, Ray
ti.init(arch=ti.cpu)

aspect_ratio = 1.0
image_height = 800
image_width = int(aspect_ratio * image_height)
pixels = ti.Vector.field(3, dtype=ti.f32, shape=(image_width, image_height))

samples_per_pixel = 4
max_depth = 10

@ti.kernel
def render():
    for i, j in pixels:
        u = (i + ti.random()) / image_width
        v = (j + ti.random()) / image_height
        color = ti.Vector([0.0, 0.0, 0.0])
        for n in range(samples_per_pixel):
            ray = camera.get_ray(u, v)
            color += ray_color(ray)
        color /= samples_per_pixel
        pixels[i, j] += color

@ti.func
def ray_color(ray):
    default_color = ti.Vector([1.0, 1.0, 1.0])
    scattered_origin = ray.origin
    scattered_direction = ray.direction
    is_hit, hit_point, hit_point_normal, front_face, material, color = scene.hit(Ray(scattered_origin, scattered_direction))
    if is_hit:
        default_color = color
    return default_color

if __name__ == '__main__':
    scene = Hittable_list()

    # Light source
    scene.add(Sphere(center=ti.Vector([0, -1, 5.4]), radius=3.0, material=0, color=ti.Vector([10.0, 10.0, 10.0])))
    # Ground
    scene.add(Sphere(center=ti.Vector([0,-1, -100.5]), radius=100.0, material=1, color=ti.Vector([0.8, 0.8, 0.8])))
    # ceiling
    scene.add(Sphere(center=ti.Vector([0, -1, 102.5]), radius=100.0, material=1, color=ti.Vector([0.8, 0.8, 0.8])))
    # back wall
    scene.add(Sphere(center=ti.Vector([0, 101, 1]), radius=100.0, material=1, color=ti.Vector([0.8, 0.8, 0.8])))
    # right wall
    scene.add(Sphere(center=ti.Vector([-101.5, -1, 0]), radius=100.0, material=1, color=ti.Vector([0.6, 0.0, 0.0])))
    # left wall
    scene.add(Sphere(center=ti.Vector([101.5, -1, 0]), radius=100.0, material=1, color=ti.Vector([0.0, 0.6, 0.0])))

    # Diffuse ball
    scene.add(Sphere(center=ti.Vector([0, -1.5, -0.2]), radius=0.3, material=1, color=ti.Vector([0.8, 0.3, 0.3])))
    # Metal ball
    scene.add(Sphere(center=ti.Vector([-0.8, -1, 0.2]), radius=0.7, material=2, color=ti.Vector([0.6, 0.8, 0.8])))
    # Glass ball
    scene.add(Sphere(center=ti.Vector([0.7, -0.5, 0]), radius=0.5, material=3, color=ti.Vector([1.0, 1.0, 1.0])))
    # Metal ball-2
    scene.add(Sphere(center=ti.Vector([0.6, -2.0, -0.3]), radius=0.2, material=2, color=ti.Vector([0.8, 0.6, 0.2])))

    camera = Camera()
    gui = ti.GUI("Ray Tracing - Color Only", res=(image_width, image_height))
    pixels.fill(0)
    cnt = 0
    while gui.running:
        render()
        cnt += 1
        gui.set_image(np.sqrt(pixels.to_numpy() / cnt))
        gui.show()

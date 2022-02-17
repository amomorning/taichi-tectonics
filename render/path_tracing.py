import taichi as ti
import numpy as np
from render_util import Hittable_list, Sphere, Camera, Ray, random_in_unit_sphere, refract, reflect, reflectance, random_unit_vector
ti.init(arch=ti.gpu)

aspect_ratio = 1.0
image_height = 800
image_width = int(aspect_ratio * image_height)
pixels = ti.Vector.field(3, dtype=ti.f32, shape=(image_width, image_height))

samples_per_pixel = 4
max_depth = 10
sample_on_unit_sphere_surface = True

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

# Path tracing
@ti.func
def ray_color(ray):
    color_buffer = ti.Vector([0.0, 0.0, 0.0])
    brightness = ti.Vector([1.0, 1.0, 1.0])
    scattered_origin = ray.origin
    scattered_direction = ray.direction
    p_RR = 0.8
    for n in range(max_depth):
        if ti.random() > p_RR:
            break
        is_hit, hit_point, hit_point_normal, front_face, material, color = scene.hit(Ray(scattered_origin, scattered_direction))
        if is_hit:
            if material == 0:
                color_buffer = color * brightness
                break
            else:
                # Diffuse
                if material == 1:
                    target = hit_point + hit_point_normal
                    if sample_on_unit_sphere_surface:
                        target += random_unit_vector()
                    else:
                        target += random_in_unit_sphere()
                    scattered_direction = target - hit_point
                    scattered_origin = hit_point
                    brightness *= color
                # Metal and Fuzz Metal
                elif material == 2 or material == 4:
                    fuzz = 0.0
                    if material == 4:
                        fuzz = 0.4
                    scattered_direction = reflect(scattered_direction.normalized(),
                                                  hit_point_normal)
                    if sample_on_unit_sphere_surface:
                        scattered_direction += fuzz * random_unit_vector()
                    else:
                        scattered_direction += fuzz * random_in_unit_sphere()
                    scattered_origin = hit_point
                    if scattered_direction.dot(hit_point_normal) < 0:
                        break
                    else:
                        brightness *= color
                # Dielectric
                elif material == 3:
                    refraction_ratio = 1.5
                    if front_face:
                        refraction_ratio = 1 / refraction_ratio
                    cos_theta = min(-scattered_direction.normalized().dot(hit_point_normal), 1.0)
                    sin_theta = ti.sqrt(1 - cos_theta * cos_theta)
                    # total internal reflection
                    if refraction_ratio * sin_theta > 1.0 or reflectance(cos_theta, refraction_ratio) > ti.random():
                        scattered_direction = reflect(scattered_direction.normalized(), hit_point_normal)
                    else:
                        scattered_direction = refract(scattered_direction.normalized(), hit_point_normal, refraction_ratio)
                    scattered_origin = hit_point
                    brightness *= color
                brightness /= p_RR
    return color_buffer


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
    gui = ti.GUI("Ray Tracing", res=(image_width, image_height))
    pixels.fill(0)
    cnt = 0
    while gui.running:
        render()
        cnt += 1
        gui.set_image(np.sqrt(pixels.to_numpy() / cnt))

        for e in gui.get_events(gui.PRESS):
            if e.key == 's':
                ti.imwrite(np.sqrt(pixels.to_numpy() / cnt), 'result.png')
        gui.show()

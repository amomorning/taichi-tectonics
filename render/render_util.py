import taichi as ti

eps = 1e-3
PI = 3.1415926


@ti.data_oriented
class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction
    @ti.func
    def at(self, t: ti.f32):
        return self.origin + t * self.direction


@ti.data_oriented
class Sphere:
    def __init__(self, center, radius, material, color):
        self.center = center
        self.radius = radius
        self.material = material
        self.color = color

    @ti.func
    def hit(self, ray, t_min=0.001, t_max=10e8):
        oc = ray.origin - self.center
        a = ray.direction.dot(ray.direction)
        b = 2.0 * ray.direction.dot(oc)
        c = oc.dot(oc) - self.radius * self.radius

        d = b * b - 4 * a * c

        hit = False
        front = False
        root = 0.0
        hit_point = ti.Vector([0.0, 0.0, 0.0])
        hit_normal = ti.Vector([0.0, 0.0, 0.0])
        if d > 0:
            sqrtd = ti.sqrt(d)
            root = (-b - sqrtd) / (2 * a)
            if(root < t_min or root > t_max):
                root = (-b + sqrtd) / (2 * a)
                if(root > t_min and root < t_max):
                    hit = True
            else:
                hit = True
        
        if hit:
            hit_point = ray.at(root)
            hit_normal = (hit_point - self.center)/self.radius
            
            if(ray.direction.dot(hit_normal) < 0):
                front = True
            else:
                hit_normal = - hit_normal
        return hit, root, hit_point, hit_normal, front, self.material, self.color
        


@ti.data_oriented
class Hittable_list:
    def __init__(self):
        self.objects = []
    def add(self, obj):
        self.objects.append(obj)
    def clear(self):
        self.objects = []

    @ti.func
    def hit(self, ray, t_min=0.001, t_max=10e8):
        closest_t = t_max
        is_hit = False
        front_face = False
        hit_point = ti.Vector([0.0, 0.0, 0.0])
        hit_point_normal = ti.Vector([0.0, 0.0, 0.0])
        color = ti.Vector([0.0, 0.0, 0.0])
        material = 1
        for index in ti.static(range(len(self.objects))):
            is_hit_tmp, root_tmp, hit_point_tmp, hit_point_normal_tmp, front_face_tmp, material_tmp, color_tmp =  self.objects[index].hit(ray, t_min, closest_t)
            if is_hit_tmp:
                closest_t = root_tmp
                is_hit = is_hit_tmp
                hit_point = hit_point_tmp
                hit_point_normal = hit_point_normal_tmp
                front_face = front_face_tmp
                material = material_tmp
                color = color_tmp
        return is_hit, hit_point, hit_point_normal, front_face, material, color

    @ti.func
    def hit_shadow(self, ray, t_min=0.001, t_max=10e8):
        is_hit_source = False
        is_hit_source_temp = False
        hitted_dielectric_num = 0
        is_hitted_non_dielectric = False
        # Compute the t_max to light source
        is_hit_tmp, root_light_source, hit_point_tmp, hit_point_normal_tmp, front_face_tmp, material_tmp, color_tmp = \
        self.objects[0].hit(ray, t_min)
        for index in ti.static(range(len(self.objects))):
            is_hit_tmp, root_tmp, hit_point_tmp, hit_point_normal_tmp, front_face_tmp, material_tmp, color_tmp =  self.objects[index].hit(ray, t_min, root_light_source)
            if is_hit_tmp:
                if material_tmp != 3 and material_tmp != 0:
                    is_hitted_non_dielectric = True
                if material_tmp == 3:
                    hitted_dielectric_num += 1
                if material_tmp == 0:
                    is_hit_source_temp = True
        if is_hit_source_temp and (not is_hitted_non_dielectric) and hitted_dielectric_num == 0:
            is_hit_source = True
        return is_hit_source, hitted_dielectric_num, 





@ti.data_oriented
class Camera:
    def __init__(self, fov=60, aspect_ratio=1.0, distance = 4.0):
        # Camera parameters
        self.position = ti.Vector.field(3, dtype=ti.f32, shape=1)
        self.lookat = ti.Vector.field(3, dtype=ti.f32, shape=1)
        self.vup = ti.Vector.field(3, dtype=ti.f32, shape=1)
        self.distance = distance
        self.fov = fov
        self.aspect_ratio = aspect_ratio

        self.cam_lower_left_corner = ti.Vector.field(3, dtype=ti.f32, shape=1)
        self.cam_horizontal = ti.Vector.field(3, dtype=ti.f32, shape=1)
        self.cam_vertical = ti.Vector.field(3, dtype=ti.f32, shape=1)
        self.reset()

    @ti.kernel
    def reset(self):
        self.position[0] = [0.0, -5.0, 1.0]
        self.lookat[0] = [0.0, -1.0, 1.0]
        self.vup[0] = [0.0, 0.0, 1.0]
        theta = self.fov * (PI / 180.0)
        half_height = ti.tan(theta / 2.0)
        half_width = self.aspect_ratio * half_height
        w = (self.position[0] - self.lookat[0]).normalized()
        v = self.vup[0].normalized()
        u = w.cross(v)

        self.cam_lower_left_corner[
            0] = self.position[0] - half_width * u - half_height * v - ((self.position[0] - self.lookat[0]).norm() / self.distance) * w 
        self.cam_horizontal[0] = 2 * half_width * u
        self.cam_vertical[0] = 2 * half_height * v

    @ti.func
    def get_ray(self, u, v):
        return Ray(self.position[0], self.cam_lower_left_corner[0] + u * self.cam_horizontal[0] + v * self.cam_vertical[0] - self.position[0])

@ti.func
def rand3():
    return ti.Vector([ti.random(), ti.random(), ti.random()])

@ti.func
def random_in_unit_sphere():
    p = 2.0 * rand3() - ti.Vector([1, 1, 1])
    while p.norm() >= 1.0:
        p = 2.0 * rand3() - ti.Vector([1, 1, 1])
    return p

@ti.func
def random_unit_vector():
    return random_in_unit_sphere().normalized()

@ti.func
def to_light_source(hit_point, light_source):
    return light_source - hit_point

@ti.func
def reflect(v, normal):
    return v - 2 * v.dot(normal) * normal

@ti.func
def refract(uv, n, etai_over_etat):
    cos_theta = min(n.dot(-uv), 1.0)
    r_out_perp = etai_over_etat * (uv + cos_theta * n)
    r_out_parallel = -ti.sqrt(abs(1.0 - r_out_perp.dot(r_out_perp))) * n
    return r_out_perp + r_out_parallel

@ti.func
def reflectance(cosine, ref_idx):
    # Use Schlick's approximation for reflectance.
    r0 = (1 - ref_idx) / (1 + ref_idx)
    r0 = r0 * r0
    return r0 + (1 - r0) * pow((1 - cosine), 5)

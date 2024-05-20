import taichi as ti
import random
ti.init(arch=ti.gpu)



res = (600, 480)

u = ti.field(dtype=ti.f32, shape=res)
v = ti.field(dtype=ti.f32, shape=res)
pixels = ti.Vector.field(3, dtype=ti.f32, shape=res)

@ti.func
def lap(a, i, j): 
    x = -a[i, j] + 0.2*(a[i-1, j] + a[i+1, j] + a[i, j-1] + a[i, j+1])
    x += 0.05 * (a[i-1, j-1] + a[i-1, j+1] + a[i+1, j-1] + a[i+1, j+1])
    return x

@ti.func
def hsv_to_rgb(h: float, s: float, v: float) -> ti.Vector:
	hh = (h / 3.1415926 * 3.0) %6	#[0, 6)
	i = ti.floor(hh)
	ff = hh - i
	p = v * (1.0 - s)
	q = v * (1.0 - (s * ff))
	t = v * (1.0 - (s * (1.0 - ff)))

	r, g, b = 0.0, 0.0, 0.0
	if i == 0: r, g, b = v, t, p
	elif i == 1: r, g, b = q, v, p
	elif i == 2: r, g, b = p, v, t
	elif i == 3: r, g, b = p, q, v
	elif i == 4: r, g, b = t, p, v
	elif i == 5: r, g, b = v, p, q
	return ti.Vector([r, g, b])

@ti.func
def constrain(value, low, high):
    ret = value
    if(ret > high): ret = high
    if(ret < low): ret = low
    return ret

@ti.kernel
def render():
    for i, j in pixels:
        x = u[i, j]
        y = v[i, j]

        F = 0.9
        k = 0.6

        du = (ti.cast(i, ti.f32)/res[0])
        dv = (ti.cast(i, ti.f32)/res[1])

        # newu = du*lap(u, i, j) - x*y*y + F*(1-x)
        # newv = dv*lap(v, i, j) + x*y*y - (F+k)*y
        newu = 0.84*lap(u, i, j) - x*y*y + 0.986*x + 0.0182
        newv = 0.29*lap(v, i, j) + x*y*y + 0.93*y

        u[i, j] = constrain(newu, 0.0, 1.0)
        v[i, j] = constrain(newv, 0.0, 1.0)

        pixels[i, j] = hsv_to_rgb(2.7+u[i,j], 0.05+ 0.05*u[i, j], 0.02+0.78*u[i, j])


gui = ti.GUI("Reaction diffusion", res)
# gui.fps_limit = 10

while gui.running:
    gui.get_event()
    if gui.is_pressed(ti.GUI.LMB):
        mouse_x, mouse_y = gui.get_cursor_pos()
        w, h = res
        x = int(w * mouse_x)
        y = int(h * mouse_y)
        
        r = random.randint(3, 20)
        for i in range(x-r, x+r):
            for j in range(y-r, y+r):
                if( (i-x)*(i-x) + (j-y)*(j-y) < r*r):
                    v[i, j] = 1.

    render()
    gui.set_image(pixels)
    gui.show()

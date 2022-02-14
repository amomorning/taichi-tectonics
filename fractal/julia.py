from matplotlib.pyplot import pause
import taichi as ti
import math
ti.init(arch=ti.gpu)

n = 800
pixels = ti.Vector.field(3, dtype=float, shape=(2*n, n))
c = ti.Vector.field(2, dtype=float, shape=1)

@ti.func
def complex_sqr(z):
    return ti.Vector([z[0]**2 - z[1]**2, z[1] * z[0] * 2])


@ti.kernel
def paint(t: float):
    for i, j in pixels:  # Parallelized over all pixels
        c[0] = ti.Vector([-0.8, ti.cos(t) * 0.2])
        z = ti.Vector([i / n - 1, j / n - 0.5]) * 2
        iterations = 0
        while z.norm() < 20 and iterations < 50:
            z = complex_sqr(z) + c[0]
            iterations += 1
        # print(iterations)
        if(iterations * 0.12 > 5.5):
            pixels[i, j] = ti.Vector([0, 0, 0])
        else:
            rgb = hsv_to_rgb(iterations * 0.12, 0.7, 1)
            pixels[i, j] = ti.Vector([rgb[0], rgb[1], rgb[2]])


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

gui = ti.GUI("Julia Set", res=(2*n , n))

i = 0
pause = False
while gui.running:

    if not pause:
        i += 1
        paint(i * 0.03)
    
    gui.set_image(pixels)
    gui.text(content=f"Space: pause", pos=(0.01, 0.98), color=0x0)
    gui.text(content=f"c = %.2f + %.2fi"%(c[0][0], c[0][1]), pos=(0.01, 0.95), color=0x0)
    for e in gui.get_events(gui.PRESS):
        if e.key == gui.ESCAPE:
            gui.running = False
        elif e.key == gui.SPACE:
            pause = not pause

    gui.show()

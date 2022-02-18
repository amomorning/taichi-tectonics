import taichi as ti
ti.init(arch=ti.gpu)

n = 800
pixels = ti.Vector.field(3, dtype=float, shape=(2*n, n))
c = ti.Vector.field(2, dtype=float, shape=1)
num = ti.field(dtype=int, shape=1)
pos = ti.field(dtype=float, shape=2)
pos[0] = -0.05
pos[1] = -0.99

@ti.func
def complex_sqr(z):
    return ti.Vector([z[0]**2 - z[1]**2, z[1] * z[0] * 2])

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


@ti.kernel
def paint(iter: int, zoom: float):
    num[0] = iter
    for i, j in pixels: 
        c[0] = ti.Vector([i/n*zoom + pos[0], j/n*zoom + pos[1]])
        z = c[0]
        iterations = 0
        while(z.norm() < 20 and iterations < num[0]):
            z = complex_sqr(z) + c[0]
            iterations += 1

        if(iterations == num[0]):
            pixels[i, j] = ti.Vector([0, 0, 0])
        else:
            rgb = hsv_to_rgb(iterations * 0.12, 0.7, 1)
            pixels[i, j] = ti.Vector([rgb[0], rgb[1], rgb[2]])


gui = ti.GUI("Mandelbrot", res=(2*n , n))
iter = gui.slider('Iterations', 5, 120, step=1)
iter.value = 100
zoom = gui.slider('Zoom', 0.1, 0, step=-0.0001)

zoom.value = 0.005

while gui.running:

    paint(int(iter.value), zoom.value)
    
    gui.set_image(pixels)
    gui.text(content=f"UP DOWN LEFT RIGHT", pos=(0.01, 0.98), color=0x0)
    gui.text(content=f"c = %.2f + %.2fi"%(c[0][0], c[0][1]), pos=(0.01, 0.95), color=0x0)
    gui.text(content=f"iterations = %d"%(num[0]), pos=(0.01, 0.92), color=0x0)

    moved = 0.002

    for e in gui.get_events(gui.PRESS):
        if e.key == gui.ESCAPE:
            gui.running = False
        elif e.key == gui.RIGHT:
            pos[0] += moved
        elif e.key == gui.LEFT:
            pos[0] -= moved
        elif e.key == gui.UP:
            pos[1] += moved 
        elif e.key == gui.DOWN:
            pos[1] -= moved
        

    gui.show()

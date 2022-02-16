
## Ray tracing in a nutshell
- Ref: [Ray tracing in one weekend](https://raytracing.github.io/books/RayTracingInOneWeekend.html)

### Empedocles
- Emission theory

![](imgs/2022-02-16-16-51-52.png)
![](imgs/2022-02-16-16-52-21.png)

### see = color * brightness
![](imgs/2022-02-16-16-56-35.png)

#### The Lambertian reflectance model
用能量守恒的观点看待反射

![](imgs/2022-02-16-16-57-48.png)
$$ \text{Brightness} = \cos(\theta) $$
![](imgs/2022-02-16-16-58-27.png)

#### The Phong reflectance model
反光方向与视线的夹角

![](imgs/2022-02-16-19-32-15.png)

$$ \text{Brightness} = (V \cdot R)^{\alpha} = (\cos(\theta)) ^{\alpha} $$
$\alpha$ is the hardness

#### The Blinn-Phong reflectance model
![](imgs/2022-02-16-19-36-42.png)
$$ \text{Brightness} = (N \cdot H)^{\alpha} = (\cos(\theta)) ^{\alpha'} , H=\frac{V+L}{||V+L||}$$
$\alpha' < \alpha$ is the hardness in Blinn-Phong
![](imgs/2022-02-16-19-37-34.png)

### The Whitted-style ray tracer
- An improved illumination model for shaded display [Whitted, 1979] [[Link]()]

#### Shadow
![](imgs/2022-02-16-19-40-34.png)
#### Reflection - Mirror
递归
![](imgs/2022-02-16-20-38-09.png)
#### Refractuion - Dielectric
![](imgs/2022-02-16-20-38-54.png)

### The Path Tracer
modern ray tracer

Global illumination(GI) 全局光照，表示漫反射表面是否继续反光
![](imgs/2022-02-16-20-43-35.png)
#### Diffuse surfaces

![](imgs/2022-02-16-20-44-15.png)
![](imgs/2022-02-16-20-45-05.png)

#### Monte Carlo method
随机 N 次估算物理量

![](imgs/2022-02-16-20-48-43.png)

N = 1, add SPP(sample per pixel)
![](imgs/2022-02-16-21-03-52.png)
#### Russian Roulette
- stop recursion by probability$p_{RR}$(for instance 90%)
- else
  - go on recursion: what is $L_i$
  - Return $L_o/p_{RR}$

### Conclusion
![](imgs/2022-02-16-21-24-26.png)

### Further readings
- The rendering equation [Kajiya 1986]

$$ L_{o}=L_{e}+\int_{\Omega} L_{i} \cdot f_{r} \cdot \cos \theta \cdot d \omega $$

- Fundamentals of Computer Graphics
- Physically Based Rendering: From Theory To Implementation
- Ray Tracing
  - In one weekend
  - The next week
  - The rest of your life
- GAMES 101
- GAMES 102

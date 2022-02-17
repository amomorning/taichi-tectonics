
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


## Ray tracing in action

### Ray casting
#### 1. Ray
- $P=0+t \overrightarrow{\boldsymbol{d}}$

![](imgs/2022-02-16-22-21-55.png)
#### 2. Positioning the camera/eye (lookfrom)
![](imgs/2022-02-16-22-23-09.png)
#### 3. Orienting the camera/eye (lookat)
![](imgs/2022-02-16-22-23-40.png)
#### 4. Placing the screen
1. `distance` from the eye to the center of the screen
2. orientation `up` of the screen

![](imgs/2022-02-16-22-24-33.png)
#### 5. Sizing the screen (field of view)
![](imgs/2022-02-16-22-26-17.png)
- `fov`: field of view $\theta$
- `aspect_ration`

![](imgs/2022-02-16-22-27-09.png)

![](imgs/2022-02-16-22-27-55.png)
![](imgs/2022-02-16-22-28-19.png)
#### 6. Ray Casting!!

![](imgs/2022-02-16-22-28-55.png)

ray across the center of a pixel
``` Python
u = float(i+0.5)/res_x
v = float(j+0.5)/res_y
```
### Ray-object intersection
![](imgs/2022-02-16-22-14-04.png)
#### Sphere
- $\|P-C\|^{2}-r^{2}=0$

![](imgs/2022-02-16-22-15-44.png)
  $$ a t^{2}+b t+c=0 \Rightarrow t=\frac{-b \pm \sqrt{b^{2}-4 a c}}{2 a}, t>\epsilon $$
- for instance, $\epsilon = 0.001$

![](imgs/2022-02-16-22-16-12.png)

#### Plane
- $(P-C)^{T} N=0$

![](imgs/2022-02-16-22-18-10.png)

- $(O+t \overrightarrow{\boldsymbol{d}}-C)^{T} N=0$

![](imgs/2022-02-16-22-19-08.png)

#### Triangle
1. intersect with triangle plane
2. inside the triangle

![](imgs/2022-02-16-22-20-12.png)

### Sampling
#### Importance Sampling
![](imgs/2022-02-17-10-14-42.png)

### Reflection and Refraction

#### The reflection coeffient: $R$
- The refraction coefficient $T = 1- R$
- material dependent
- view point dependent

##### Fresnel's Equation
- s-polarization 
  $$R_{S}=\left(\frac{n_{1} \cos \left(\theta_{i}\right)-n_{2} \cos \left(\theta_{t}\right)}{n_{1} \cos \left(\theta_{i}\right)+n_{2} \cos \left(\theta_{t}\right)}\right)^{2}$$
- P-polarization 
  $$R_{P}=\left(\frac{n_{1} \cos \left(\theta_{t}\right)-n_{2} \cos \left(\theta_{i}\right)}{n_{1} \cos \left(\theta_{t}\right)+n_{2} \cos \left(\theta_{i}\right)}\right)^{2}$$
- For "natural light" 
  $$R=\frac{1}{2}\left(R_{S}+R_{P}\right)$$

##### Schlick's approximation
$$R\left(\theta_{i}\right)=R_{0}+\left(1-R_{0}\right)\left(1-\cos \left(\theta_{i}\right)\right)^{5}$$
$$R_{0}=\left(\frac{n_{1}-n_{2}}{n_{1}+n_{2}}\right)^{2}$$


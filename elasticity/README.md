# Elasticity

## Time integration

### Explicit (forward) Euler integration （前向欧拉法）

$$ \begin{aligned}
&x_{n+1}=x_{n}+h v_{n} \\
&v_{n+1}=v_{n}+h M^{-1} f\left(x_{n}\right)
\end{aligned} $$

extremely fast, but will also increase the system energy...
therefore seldom used

### Symplectic Euler integration （辛欧拉法）

从辛几何推导而来，比较长期维持系统稳定，当 $h$ 越来越大会有些形变

$$ \begin{aligned}
&v_{n+1}=v_{n}+h M^{-1} f\left(x_{n}\right) \\
&x_{n+1}=x_{n}+h v_{n+1}
\end{aligned} $$

辛欧拉法才是在实际使用中称为"前向欧拉"的真正公式

### Implicit (backward) Euler integration

$$ \begin{aligned}
&v_{n+1}=v_{n}+h M^{-1} f\left(x_{n+1}\right) \\
&x_{n+1}=x_{n}+h v_{n+1}
\end{aligned} $$

随着时间积分，系统能量会慢慢减小，自带数值阻尼，时间越长

### Pipeline of time integration

- Time integration steps:
  - Evaluate $f$ at $x_n$
    - for conservative force: $f(x) = -E(x)$, where $E$ is the potential energy
  - Update $v$ using $f$ (or $M^{-1}f$
  - Update $x$ using $v$

#### Example: galaxy system

Gravitational energy:
$$E=-\frac{G M m}{r\left(x_{1}, x_{2}\right)}$$
Gradient:
$$\frac{\partial E}{\partial x_{1}}=\frac{\partial r}{\partial x_{1}} \cdot \frac{\partial E}{\partial r}=\frac{x_{1}-x_{2}}{r} * \frac{G M m}{r^{2}}$$
$$f(x_1)=-\frac{\partial E}{\partial x_{1}}$$
$$f(x_2)=-\frac{\partial E}{\partial x_{2}}=-f(x_1)$$

对于能量系统，对能量求导可以得到力，力可以得到加速度，就可以对速度进行更新，得到下一帧的位置。

The energy is all we need!!!

而弹性物体需要对连续介质进行空间的积分：

### the spatial integration

空间积分基于两种离散化方式：

- 弹簧质点系统
- 线性有限元

#### Mass spring system

1. 对连续介质进行离散化
2. 将质量分布到顶点上得到质点
3. 使用弹簧连接所有的质点

![img](imgs/2022-02-23-14-05-18.png)

弹簧的存在使得物体发生形变时会有回到原来形状的趋势

##### Define deformation

- spring current pose: $x_1, x_2$
- spring current length: $l=\left\|x_1-x_2\right\|$
- rest-length: $l_0$
- deformation: $l-l_0$

##### Hooke's Law

$$E\left(x_{1}, x_{2}\right)=\frac{1}{2} k\left(l-l_{0}\right)^{2}$$

Gradient: 
$$\frac{\partial E}{\partial x_{1}}=\frac{\partial l}{\partial x_{1}} \cdot \frac{\partial E}{\partial l}=\frac{x_{1}-x_{2}}{l_{0}} * k\left(l-l_{0}\right)$$

$$f(x_1)=-\frac{\partial E}{\partial x_{1}}$$

$$f(x_2)=-f(x_1)$$

![](imgs/2022-02-23-14-13-46.png)

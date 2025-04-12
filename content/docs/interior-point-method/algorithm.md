---
weight: 430
title: "内点法"
description: ""
icon: "article"
date: "2025-04-12T09:14:38+08:00"
lastmod: "2025-04-12T09:14:38+08:00"
draft: true
toc: true
katex: true
---

## 中心路径

回顾问题 $\text{(PP)}$，它在 $\mathcal{F}^{\circ}(P)$ 中最小化最小化 $B_{\mu}(x)$，即
$$
\begin{aligned}
\min~ & c^Tx + \mu F(x)\\
\text{s.t. } & Ax = b\\
& x > 0
\end{aligned} \quad\quad  (\text{PP})
$$
我们已知它最优解的充要条件，而且可以用牛顿法求它的最优解。

但是，给定 $\mu > 0$，$\text{(PP)}$ 的最优解并不是原问题 $\text{(P)}$ 的最优解。因此，迭代的目标不是求解 $\text{(PP)}$ ，而是去逼近原问题 $\text{(P)}$ 的最优解。逼近的方式就是在迭代中不断减小 $\mu$ 值，然后更新下降方向；当 $\mu$ 足够小时，得到的解与原问题的最优解足够接近。

具体来说，给定初始值 $\mu^0 > 0$ 和初始点 $x^0(\mu^0), y^0(\mu^0), s^0(\mu^0) \in \mathcal{F}^{\circ}(P)\times \mathcal{F}^{\circ}(D)$ ，迭代过程得到如下的点列：
$$
x^0(\mu^0), y^0(\mu^0), s^0(\mu^0),\\
x^1(\mu^1), y^1(\mu^1), s^1(\mu^1),\\
\vdots\\
x^k(\mu^k), y^k(\mu^k), s^k(\mu^k)\\
$$
其中 $\mu^0 > \mu^1 > \dots > \mu^k$。当 $\mu^k < \epsilon$ 时，迭代停止，其中 $\epsilon > 0$ 代表逼近的精度。

我们把 $\{x(\mu),y(\mu),s(\mu): \mu > 0\}$ 称为 **中心路径**（Central Path）。迭代的过程就是沿着中心路径，令 $\mu$ 值不断减小的过程，这样的算法也称为 *路径跟踪*（Path Following）。

## 内点法（理论版）

接下来介绍具体的迭代步骤。

**原始对偶内点法 (Primal-Dual Interior Point Method)**

---

第一步，初始化 $\mu^0,x^0,y^0,s^0$。注意： $\mu, x, s >0$ 且 $x^0,y^0,s^0$ 可行。

第二步，判断误差：如果 $\mu < \epsilon$ 则停止。

第三步，计算牛顿方向：
$$
\begin{bmatrix}
A & 0 & 0 \\
0 & A^T & I \\
S & 0 & X
\end{bmatrix}\begin{bmatrix}
\Delta x\\
\Delta y\\
\Delta s
\end{bmatrix} = -\begin{bmatrix}
0\\
0\\
XSe-\mu e
\end{bmatrix}
$$
第四步，更新 $x, y, s$：
$$
(x,y,s) \leftarrow (x,y,s) + (\Delta x, \Delta y, \Delta s)
$$
第五步，减小 $\mu$ 值，令 $\mu \leftarrow \sigma \cdot \mu$，其中 $\sigma \in [0,1]$， 然后执行第二步。

---

这里还有几个问题需要回答：

1. $\mu$ 和 $\sigma$ 值如何选取？

2. 第四步更新 $x,y,s$ 之后，它还是可行解吗？

3. 如何计算初始可行解 $x^0,y^0,s^0$ ？ 

先看第一个问题。

先计算原问题 $\text{(P)}$ 和对偶问题 $\text{(D)}$ 的对偶间隙 (Duality Gap)：
$$
c^Tx - b^Ty = (A^Ty + s)^Tx - b^Ty = s^Tx
$$
令 $\mu = \frac{s^Tx}{n}$，当 $\mu < \epsilon$ 时，我们有 $c^Tx - b^Ty \leq n \epsilon$，即目标函数值与最优值当误差不超过 $n\epsilon$。

此外，令 $\sigma = 1- \frac{0.4}{\sqrt{n}}$，可以证明最多 $O(\sqrt{n}\ln(1/\epsilon))$ 次迭代，就可以使得 $\mu < \epsilon$。

再看第二个问题。

只需要验证 $x+\Delta x$ 与 $(y+\Delta y, s+\Delta s)$ 是否满足原始问题和对偶问题的约束：
$$
\begin{aligned}
& A(x+\Delta x) = b + A\Delta x = b\\
& A^T(y +\Delta y) + (s + \Delta s) =c + A^T\Delta y + \Delta s = c
\end{aligned}
$$
因此答案是肯定的。

关于第三个问题，计算初始可行解并不容易，这里不做介绍。原因是在实际应用中，可以通过逼近的方式满足可行性，因而初始解只要保证 $x,s>0$ 即可。

## 内点法（实践版）

编程实现内点法时，一般不会严格按照上面的理论版，原因是效率不高。

下面介绍一个实践版本。

---

第一步，初始化 $x^0 > 0,s^0 >0, y^0$，令 $\mu = \frac{s^Tx}{n}$。

第二步，判断误差：如果 $\mu < \epsilon$ 则停止，其中
$$
\mu = \max \{||Ax-b||, ||A^Ty+s-c||, ||s^Tx||\}
$$
第三步，计算牛顿方向：
$$
\begin{bmatrix}
A & 0 & 0 \\
0 & A^T & I \\
S & 0 & X
\end{bmatrix}\begin{bmatrix}
\Delta x\\
\Delta y\\
\Delta s
\end{bmatrix} = -\begin{bmatrix}
Ax-b\\
A^Ty + s - c\\
XSe-\mu e
\end{bmatrix}
$$
第四步，更新 $x, y, s$：
$$
\begin{aligned}
& x \leftarrow x + \alpha_P \cdot \Delta x \\
& (y,s) \leftarrow (y,s) + \alpha_D \cdot (\Delta y, \Delta s)
\end{aligned}
$$
其中 $\alpha_P, \alpha_D$ 使得 $x,s>0$，即
$$
\alpha_P = \min \left\{1, \min_{\Delta x_j < 0} \left\{\frac{x_j}{-\Delta x_j}\right\}\right\}\\
\alpha_D = \min \left\{1, \min_{\Delta s_j < 0} \left\{\frac{s_j}{-\Delta s_j}\right\}\right\}
$$
第五步，减小 $\mu$ 值，令 $\mu \leftarrow \sigma \cdot \mu$，其中 $\sigma = 0.1$ (经验值)， 然后执行第二步。

---

注意两点变化：

第一，初始解不要求可行，原因是可以通过迭代的方式保障可行性。它通过 $\mu$ 的选择来实现，它是三种误差的最大值，即原问题的可行性误差 $||Ax-b||$， 对偶问题的可行性误差 $||A^Ty + s-c||$，以及目标函数误差 $s^Tx$。 当 $\mu < \epsilon$ 且 $\epsilon$ 精度足够小时，原问题和对偶问题可行，并且目标函数值达到最优。

第二，由于迭代过程中，原始解和对偶解可能不满足可行性，因此更新 $x,y,s$ 的步长 $\alpha$ 需要保证 $x,s>0$。其中 $x$ 与 $(y,s)$ 也可以采用相同的步长，例如 $\alpha = \min (\alpha_D, \alpha_P)$。


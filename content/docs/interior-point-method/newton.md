---
weight: 420
title: "牛顿法"
description: ""
icon: "article"
date: "2025-04-12T09:20:08+08:00"
lastmod: "2025-04-12T09:20:08+08:00"
draft: false
toc: true
katex: true
---

解下面这个方程。

{{<katex>}}
$$
F(x,y,s) := \begin{bmatrix}
Ax-b\\
A^Ty + s - c\\
XSe-\mu e
\end{bmatrix} = \mathbf{0}
$$
{{</katex>}}

其中 $A, b, c,\mu$ 是参数，$e$ 是常量，$x, y, s, X, S$ 是变量。

它们的定义如下。

{{<katex>}}
$$
\begin{aligned}
& A\in\mathbb{R}^{m\times n}, ~b\in\mathbb{R}^m, ~c\in\mathbb{R}^n,~ \mu > 0, ~ \mu \in \mathbb{R}^n, n\geq m \\[6pt]
& e = [1, 1, ..., 1]^T \in \mathbb{R}^n, \\[6pt]
& x, s\in \mathbb{R}^n, ~ y\in\mathbb{R}^m, \\[6pt]
& X = 
\begin{bmatrix}
x_1 & 0 & \cdots & 0 \\
0 & x_2&  \cdots & 0\\
\vdots & \vdots & \ddots & \vdots\\
0 & 0 & \cdots & x_n 
\end{bmatrix}, ~
S = 
\begin{bmatrix}
s_1 & 0 & \cdots & 0 \\
0 & s_2&  \cdots & 0\\
\vdots & \vdots & \ddots & \vdots\\
0 & 0 & \cdots & s_n 
\end{bmatrix}
\end{aligned}
$$
{{</katex>}}

此外，$A$ 的秩为 $m$。

### 思路

简单介绍一下用牛顿法解方程的思路。已知方程 $f(x) = 0$ 且 $f(x)$ 连续可导。

用 $f(x)$ 在点 $x^k$ 的一阶泰勒展式去近似它。

{{<katex>}}
$$
f(x) \approx f(x^k) + f'(x^k)(x-x^k)
$$
{{</katex>}}

那么
{{<katex>}}
$$
f(x^{k+1}) \approx f(x^k) + f'(x^k)(x^{k+1} -x^k)
$$
{{</katex>}}

根据方程 $f(x) = 0$，我们有

{{<katex>}}
$$
f(x^k) + f'(x^k)(x^{k+1} -x^k) = 0
$$
{{</katex>}}

因此

{{<katex>}}
$$
x^{k+1} = x^k   - \frac{f(x^k)}{f'(x^k)}
$$
{{</katex>}}

根据 $x^k$ 计算 $x^{k+1}$，这就是迭代公式。

从第 $x^0$ 开始，得到 $x^1, x^2, ...$，持续迭代下去，直到$|f(x^{k}) - f(x^{k-1})| \rightarrow 0$ 时停止。

### 迭代

考虑方程 $F(x, y, s) = \mathbf{0}$。已知 $x^k, y^k, s^k$，要计算 $x^{k+1}, y^{k+1}, s^{k+1}$。

回顾上面的思路。牛顿法需要计算方程的一阶导数。由于 $F$ 是一个向量函数。这种情况下，它在 $x^k, y^k, s^k$ 的一阶导数就是 $F$ 的雅可比矩阵 $J$。

{{<katex>}}
$$
J(x^k,y^k,s^k) = \begin{bmatrix}
\frac{\partial F_1}{\partial x} & \frac{\partial F_1}{\partial y} & \frac{\partial F_1}{\partial s}\\[6pt]
\frac{\partial F_2}{\partial x} & \frac{\partial F_2}{\partial y} & \frac{\partial F_2}{\partial s}\\[6pt]
\frac{\partial F_3}{\partial x} & \frac{\partial F_3}{\partial y} & \frac{\partial F_3}{\partial s}
\end{bmatrix} = \begin{bmatrix}
A & 0 & 0 \\
0 & A^T & I \\
A & 0 & 0 \\
S^k & 0 & X^k
\end{bmatrix}
$$
{{</katex>}}

其中 $F_1, F_2, F_3$ 分别代表函数值的第 $1, 2, 3$ 个分量

{{<katex>}}
$$
\begin{aligned}
& X^k = 
\begin{bmatrix}
x_1^k & 0 & \cdots & 0 \\
0 & x_2^k &  \cdots & 0\\
\vdots & \vdots & \ddots & \vdots\\
0 & 0 & \cdots & x_n^k 
\end{bmatrix}, ~
S^k = 
\begin{bmatrix}
s_1^k & 0 & \cdots & 0 \\
0 & s_2 ^k&  \cdots & 0\\
\vdots & \vdots & \ddots & \vdots\\
0 & 0 & \cdots & s_n ^k
\end{bmatrix}
\end{aligned}
$$
{{</katex>}}

根据下面的线性方程组来计算 $x^{k+1}, y^{k+1}, s^{k+1}$。

{{<katex>}}
$$
J(x^k,y^k,s^k)\begin{bmatrix}
x^{k+1} -x^k\\
y^{k+1} - y^k\\
s^{k+1} - s^k
\end{bmatrix} + F(x,y,s) = 0
$$
{{</katex>}}

引入记号（称为**牛顿方向**）

{{<katex>}}
$$
\begin{aligned}
& \Delta x^k := x^{k+1} - x^k \\
& \Delta y^k := y^{k+1} - y^k \\
& \Delta s^k := s^{k+1} - s^k \\
\end{aligned}
$$
{{</katex>}}

上面的方程可以写成

{{<katex>}}
$$
\begin{bmatrix}
A & 0 & 0 \\
0 & A^T & I \\
S^k & 0 & X^k
\end{bmatrix}\begin{bmatrix}
\Delta x^k\\
\Delta y^k\\
\Delta s^k
\end{bmatrix} = -\begin{bmatrix}
Ax^k-b\\
A^Ty^k + s^k - c\\
X^kS^ke-\mu e
\end{bmatrix}
$$
{{</katex>}}

由于 $x^k, y^k$ 是可行解，上式可以写成

{{<katex>}}
$$
\begin{bmatrix}
A & 0 & 0 \\
0 & A^T & I \\
S^k & 0 & X^k
\end{bmatrix}\begin{bmatrix}
\Delta x^k\\
\Delta y^k\\
\Delta s^k
\end{bmatrix} = -\begin{bmatrix}
0\\
0\\
X^kS^ke-\mu e
\end{bmatrix}
$$
{{</katex>}}

解出 $x^k, y^k, s^k$，我们就得到 

{{<katex>}}
$$
\begin{aligned}
& x^{k+1} = x^k + \Delta x^k\\
& y^{k+1} = y^k + \Delta y^k\\
& s^{k+1} = s^k + \Delta s^k\\
\end{aligned}
$$
{{</katex>}}

计算 $x^k, y^k, s^k$ 从 $k=0, 1, 2, ...$ 直到满足停止条件。

$$
\left|F(x^k, y^k, s^k) - F(x^{k-1}, y^{k-1}, s^{k-1})\right | < \epsilon
$$

其中 $\epsilon > 0$ 是一个很小的常数。




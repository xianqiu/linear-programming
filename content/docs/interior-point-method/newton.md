---
weight: 420
title: "牛顿法"
description: ""
icon: "article"
date: "2025-04-12T09:20:08+08:00"
lastmod: "2025-04-12T09:20:08+08:00"
draft: true
toc: true
katex: true
---

考虑下面这个方程。

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
0 & x_1&  \cdots & 0\\
\vdots & \vdots & \ddots & \vdots\\
0 & 0 & \cdots & x_n 
\end{bmatrix}, ~
S = 
\begin{bmatrix}
s_1 & 0 & \cdots & 0 \\
0 & s_1&  \cdots & 0\\
\vdots & \vdots & \ddots & \vdots\\
0 & 0 & \cdots & s_n 
\end{bmatrix}
\end{aligned}
$$
{{</katex>}}

此外，$A$ 的秩为 $m$。

### 迭代

可以用牛顿法迭代法求解上面的方程 $F(x,y,s)=0$。

这里只介绍牛顿法的基本步骤。记 $x^k, y^k, s^k$ 代表第 $k$ 步的迭代结果，那么
{{<katex>}}
$$
(x^{k+1}, y^{k+1}, s^{k+1}) = (x^k,y^k, s^k) + \alpha^k \cdot (\Delta x^k, \Delta y^k, \Delta s^k)
$$
{{</katex>}}
其中 $(\Delta x^k, \Delta y^k, \Delta s^k)$ 代表迭代方向，$\alpha^k\in (0,1]$ 代表步长。

令 $J(x,y,s)$ 代表 $F(x,y,s)$ 的雅可比矩阵，即
{{<katex>}}
$$
J(x,y,s) = \begin{bmatrix}
\frac{\partial F_1}{\partial x} & \frac{\partial F_1}{\partial y} & \frac{\partial F_1}{\partial s}\\
\frac{\partial F_2}{\partial x} & \frac{\partial F_2}{\partial y} & \frac{\partial F_2}{\partial s}\\
\frac{\partial F_3}{\partial x} & \frac{\partial F_3}{\partial y} & \frac{\partial F_3}{\partial s}
\end{bmatrix} = \begin{bmatrix}
A & 0 & 0 \\
0 & A^T & I \\
A & 0 & 0 \\
S & 0 & X
\end{bmatrix}
$$
{{</katex>}}

求解下面的线性方程组：

{{<katex>}}
$$
J(x,y,s)\begin{bmatrix}
\Delta x\\
\Delta y\\
\Delta s
\end{bmatrix} + F(x,y,s) = 0
$$
{{</katex>}}
即，
{{<katex>}}
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
{{</katex>}}

可以得到牛顿法的迭代方向。

由于 $x, y$ 是可行解，上式可以写成

{{<katex>}}
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
{{</katex>}}
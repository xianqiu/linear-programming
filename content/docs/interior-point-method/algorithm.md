---
weight: 430
title: "内点法"
description: ""
icon: "article"
date: "2025-04-12T09:14:38+08:00"
lastmod: "2025-04-12T09:14:38+08:00"
draft: false
toc: true
katex: true
---

考虑标准的线性规划问题。

{{<katex>}}
$$
\begin{aligned}
\min~ & c^Tx\\
\text{s.t. } & Ax=b\\
& x\geq 0
\end{aligned}
$$
{{</katex>}}

其中 $A\in\mathbb{R}^{m\times n}$ 满秩，$b \in\mathbb{R}^m$，$c, x \in\mathbb{R}^n$，$n\geq m$。

我们不直接求解它，而是通过下面这个 **近似问题** 来逼近。

{{<katex>}}
$$
\begin{aligned}
\min~ & c^Tx - \mu \sum_{j=1}^n \ln (x_j) \\
\text{s.t. } & Ax = b\\
& x > 0
\end{aligned}
$$
{{</katex>}}

在求解过程中不断减小 $\mu$ 值，使得近似问题与原问题的最优解就足够接近。

### 牛顿方向

解上面这个近似问题，它的 [最优解](optimality) 需要满足如下线性方程组。

{{<katex>}}
$$
F(x,y,s) = 
\begin{bmatrix}
Ax-b\\
A^Ty + s - c\\
XSe-\mu e
\end{bmatrix} = \mathbf{0}
$$
{{</katex>}}

我们可以用 [牛顿法](newton) 求解。

已知 $x^k, y^k, s^k$，需要计算 $x^{k+1}, y^{k+1}, s^{k+1}$。

① 计算牛顿方向 $\Delta x^k, \Delta y^k, \Delta s^k$。

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
\mathbf{0} \\
\mathbf{0} \\
X^kS^ke-\mu e
\end{bmatrix}
$$
{{</katex>}}

② 得到 $x^{k+1}, y^{k+1}, s^{k+1}$。

{{<katex>}}
$$
\begin{aligned}
& x^{k+1} = x^k + \Delta x^k\\
& y^{k+1} = y^k + \Delta y^k\\
& s^{k+1} = s^k + \Delta s^k\\
\end{aligned}
$$
{{</katex>}}

持续迭代，直到满足停止条件。

## 算法描述

**第一步：初始化**

令 $x^0, y^0, s^0$ 代表迭代的起点。它们是原问题和对偶问题的内点，因此是可行解。但是这样的起点不容易找。在实际中，可以放松这个要求。只需要满足 $x^0 >0, s^0 > 0$。迭代过程中随着 $\mu$ 越来越小，对应的解收敛到可行解。

根据 $F(x,y,s) =\mathbf{0}$，我们有
$$
XSe -\mu e =\mathbf{0} \Rightarrow x^T s = n \cdot \mu
$$

我们有

$$
\mu =\frac{x^Ts}{n} = \frac{(x^0)^Ts^0}{n}
$$

**第二步：判断停止条件**

令 $\epsilon = 10^{-8}$。当如下条件满足时，得到最优解，算法停止。

{{<katex>}}
$$
\max \{||Ax-b||,~ ||A^Ty+s-c||,~||x^Ts||\} < \epsilon
$$
{{</katex>}}

前面两项保证可行性。解释一下第三项，它是原问题与对偶问题目标函数的差值。

{{<katex>}}
$$
\begin{aligned}
&~ c^Tx - b^Ty \\
= &~ (A^Ty + s)^Tx - b^Ty \\
= &~ s^Tx
\end{aligned}
$$
{{</katex>}}

根据对偶理论，如果 $s^Tx =  0$，那么 $x, y, s$ 是最优解。

**第三步：缩小 $\mu$ 值**

令 $\mu := \alpha \cdot \mu$，其中 $\alpha\in [0,1]$ 是一个缩放因子。例如取 $\alpha=0.1$。

**第四步： 计算牛顿方向**

根据下面的方程计算牛顿方向。

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

等式右边前两项没有写成 $\mathbf{0}$，原因是当前的 $x,y,s$ 可能不是可行解。但是在后续的迭代中，它会逐步变成可行解。

**第五步，更新 $x, y, s$**

{{<katex>}}
$$
\begin{aligned}
& x := x + \alpha_P \cdot \Delta x \\
& y := y + \alpha_D \cdot \Delta y \\
& s := s + \alpha_D \cdot \Delta s 
\end{aligned}
$$
{{</katex>}}

其中 $\alpha_P, \alpha_D$ 作用是保证 $x,s>0$。

它们的取值如下所示。

{{<katex>}}
$$
\alpha_P = \min \left\{1,~ r\min_{\Delta x_j < 0} \left\{\frac{x_j}{-\Delta x_j}\right\}\right\}\\[6pt]
\alpha_D = \min \left\{1,~ r\min_{\Delta s_j < 0} \left\{\frac{s_j}{-\Delta s_j}\right\}\right\}
$$
{{</katex>}}

其中 $0<r<1$，一般取 $r=0.99$。

回到**第二步**。

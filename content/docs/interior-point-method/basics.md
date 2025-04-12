---
weight: 410
title: "基本概念"
description: ""
icon: "article"
date: "2025-04-12T08:48:15+08:00"
lastmod: "2025-04-12T08:48:15+08:00"
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

### 对偶问题

下面是它的**对偶问题**。

{{<katex>}}
$$
\begin{aligned}
\max~ & b^Ty\\
\text{s.t. } & A^Ty \leq c\\
\end{aligned}
$$
{{</katex>}}

其中 $y\in\mathbb{R}^m$。

引入松弛变量 $s$，对偶问题可以写成这样。

{{<katex>}}
$$
\begin{aligned}
\max~ & b^Ty\\
\text{s.t. } & A^Ty + s = c\\
& s\geq 0
\end{aligned}
$$
{{</katex>}}

### 内点

单纯形算法是从顶点出发，迭代到最优解。而内点法是从内点出发，然后逼近最优解。内点和顶点的共同点是，它们都是可行解。区别在于，内点一般不是基本可行解。因此，最后内点法得到的最优解实际上是原问题最优解的一个近似解。

接下来介绍内点的定义。

令 $\mathcal{F}_P, \mathcal{F}_D$ 分别代表原问题和对偶问题的可行区域。

{{<katex>}}
$$
\begin{aligned}
& \mathcal{F}_P =\{x\mid Ax=b,~ x\geq0\}\\
& \mathcal{F}_D = \{(y,s)\mid A^Ty+s=c, ~ s\geq 0\}
\end{aligned}
$$
{{</katex>}}

用记号 $\mathcal{F}^{\circ}_P$ 或  $\mathcal{F}^{\circ}_D$  代表可行域的 **内部（Interior）**，其中的点就称为 **内点（Interior Point）**。

{{<katex>}}
$$
\begin{aligned}
& \mathcal{F}^{\circ}_P =\{x \mid Ax=b, ~ x > 0\}\\
& \mathcal{F}^{\circ}_D = \{(y,s)\mid A^Ty + s =c, ~ s > 0\}
\end{aligned}
$$
{{</katex>}}

### 罚函数

接下来对原问题的目标函数做一个修改。目的是让问题的最优解变成一个内点。这样一来，就可以让迭代始终在在可行域的内部。

定义一个 **罚函数（Penalty Function）**，或者也称为 **障碍函数 （Barrier Function）**。

$$
F(x) = -\sum_{j=1}^n \ln(x_j)
$$

当 $x\rightarrow 0$ 时，$F(x) \rightarrow \infty$。简单来说，$x$ 越靠近边界 $0$，函数值越大。

把它加入目标函数，我们得到

$$
\min~ c^Tx + F(x)
$$

当 $x\rightarrow 0$ 时，目标函数会增大。从而保证最优解在可行域内部。但问题来了，这不仅改变了目标函数值，而且最优解也变了。换句话说，我们得到了一个新问题。这个新问题跟原问题是不同的。

为了解决这个麻烦。引入一个参数 $\mu > 0$。重新定义这个目标函数。

$$
\min~ g_{\mu} (x) := c^Tx + \mu\cdot F(x)
$$

从上式可以看到，当 $\mu\rightarrow 0$ 时，$g_{\mu}(x)\rightarrow c^Tx$。 

换句话说，可以用 $\mu$ 来控制原问题与新问题目标函数的距离。迭代的过程中，只要不断地减小 $\mu$ 值，就能逼近原问题的最优目标函数值。

### 近似问题

考虑下面这个问题。

{{<katex>}}
$$
\begin{aligned}
\min~ & c^Tx + \mu F(x)\\
\text{s.t. } & Ax = b\\
& x > 0
\end{aligned}
$$
{{</katex>}}

它的可行解 $x$ 是原问题的内点，即 $x\in \mathcal{F}^0_P$。它的目标函数值比原问题的目标函数值大 $\mu F(x)$。

如果对任意的 $\mu >0$，能求这个问题的最优解。那么只要 $\mu \rightarrow 0$，也就相当于求得原问题的最优解。




---
weight: 723
title: "行生成"
description: ""
icon: "article"
date: "2025-03-22T17:08:12+08:00"
lastmod: "2025-03-22T17:08:12+08:00"
draft: false
toc: true
katex: true
---

考虑设施选址问题的数学规划。

{{<katex>}}
$$
\begin{aligned}
\min ~  & \sum_{i=1}^m f_iy_i + \sum_{i=1}^m\sum_{j=1}^n c_{ij}x_{ij}\\[6pt]
\text{s.t. } & \sum_{i=1}^m x_{ij} = 1, \quad \forall j\\[6pt]
& x_{ij}\leq y_i, \quad \forall i, j\\[6pt]
& x_{i,j}\geq 0,~ y_i \in \set{0,1}, \quad \forall i, j
\end{aligned}
$$
{{</katex>}}

如果问题规模很大，直接求解不可行的时候，可以用间接的办法。思路是把原问题分解成规模更小的问题。

### 子问题

在上面的问题中，决策变量有 $x$ 和 $y$，其中 $x$ 是连续变量，$y$ 是整数变量。如果已知 $y$ 值，那么问题就是关于 $x$ 的连续问题。直观的想法就是把问题按 $x$ 和 $y$ 分开。

先考虑 $x$ 部分，把 $y$ 当作输入。

**`LP1 -- Linear Program 1`**

{{<katex>}}
$$
\begin{aligned}
\min ~  & \sum_{i=1}^m\sum_{j=1}^n c_{ij}x_{ij}\\[6pt]
\text{s.t. } & \sum_{i=1}^m x_{ij} = 1, \quad \forall j\\[6pt]
& x_{ij}\leq \textcolor{blue}{y_i}, \quad \forall i, j\\[6pt]
& x_{i,j}\geq 0, \quad \forall i, j
\end{aligned}
$$
{{</katex>}}

这里有个问题，$y$ 值从哪里来。我们看原问题，计算 $y$ 需要 $x$，但 $x$ 又依赖 $y$。因为在上式中，$y$ 在约束条件中。这样就循环依赖了。


为了处理这个麻烦，我们先把 `LP1` 换一个写法。定义对偶变量 $\alpha_j$ 和 $\beta_{ij}$，它的 [对偶问题](../../modeling/write-dual) 如下所示。

**`DP1 - Dual Program 1`**
{{<katex>}}
$$
\begin{aligned}
\max ~  & \sum_{j=1}^n \alpha_j - \sum_{i=1}^m \sum_{j=1}^n \textcolor{blue}{y_i} \beta_{ij}\\[6pt]
\text{s.t. } & \alpha_j -\beta_{ij} \leq c_{ij}, \quad \forall i,j\\[6pt]
& \beta_{ij} \geq 0, \quad \forall i, j
\end{aligned}
$$
{{</katex>}}

假设 `LP1` 存在最优解。根据根据对偶理论，那么 `LP1` 和 `DP1` 的最优目标函数值相等。也就是说，`DP1` 是  `LP1` 的等价形式。

`DP1` 就是我们的**子问题**。已知 $y$ 值，可以求解最优的 $\alpha, \beta$ 值。这个形式的好处是，参数 $y$ 的位置从原来 `LP1` 中的约束位置，变到了现在  `DP1` 中的目标位置。换句话说，问题 `DP1` 的可行域不再依赖 $y$ 值。

### 主问题

把 `DP1` 的最优目标函数值代入原问题。原问题可以写成得到如下形式。

{{<katex>}}
$$
\begin{aligned}
\min ~ \left\{\sum_{i=1}^m f_iy_i + z \right\}
\end{aligned}
$$
{{</katex>}}

其中

{{<katex>}}
$$
z = 
\max~ \left\{\sum_{j=1}^n \alpha_j - \sum_{i=1}^m \sum_{j=1}^n y_i \beta_{ij} ~\mid ~ \alpha_j-\beta_{ij}\leq c_{ij}, \beta_{ij}\geq 0\right\}
$$
{{</katex>}}

为了简化形式，我们把上式中的 $\alpha,\beta$ 值用一个集合 $F$ 表示。

{{<katex>}}
$$
F = \left\{(\alpha_j, \beta_{ij}) |~ \alpha_j - \beta_{ij} \leq c_{ij}, \beta_{ij}\geq 0, \forall i,j \right\}
$$
{{</katex>}}

这样一来，原问题可以写成。

**`IP2 - Integer Program 2`**
{{<katex>}}
$$
\begin{aligned}
\min ~  & \sum_{i=1}^m f_iy_i + z\\[6pt]
\text{s.t. } & \sum_{j=1}^n \textcolor{blue}{\alpha_j} -\sum_{i=1}^m\sum_{j=1}^n y_i \textcolor{blue}{\beta_{ij}} \leq z, \quad \forall (\alpha_j, \beta_{ij}) \in F\\
&y_{i} \in \set{0,1}, ~ z\geq0\quad \forall i
\end{aligned}
$$
{{</katex>}}

其中 $\alpha_j, \beta_{ij}$ 是参数，$z, y_i$ 是决策变量。

在这个形式下，没法直接求解，因为约束有无穷多个。换句话说，满足 $F$ 中条件的 $\alpha, \beta$ 值有无穷多个。

但是可以近似地求解。考虑它的一部分约束 $F_0\subseteq F$，对应的最优目标函数值，就是原问题最优目标函数值的下界。

根据这样的观察，定义下面的**主问题**。

**`IP3 - Integer Program 3`**

{{<katex>}}
$$
\begin{aligned}
\min ~  & \sum_{i=1}^m f_iy_i + z\\[6pt]
\text{s.t. } & \sum_{j=1}^n \textcolor{blue}{\alpha_j} -\sum_{i=1}^m\sum_{j=1}^n y_i \textcolor{blue}{\beta_{ij}} \leq z, \quad \forall (\alpha_j, \beta_{ij}) \in \textcolor{red}{F_0}\\
&y_{i} \in \set{0,1},~ z\geq0 \quad \forall i
\end{aligned}
$$
{{</katex>}}

其中 $F_0$ 是 $F$ 的子集。

`IP3` 与 `IP2` 只有约束的区别。`IP3` 只考虑 `IP2` 的一部分约束，可以看作是原问题的近似问题。在迭代的过程中，我们会逐步增加约束的数量，那么其最优目标函数值就会逐渐增加。换句话说，随着约束的增加，其最优目标函数值逐步逼近最优目标函数值。

现在我们有了主问题 `IP3` 和子问题 `DP1`。其中 `IP3` 是一个整数规划问题，它的输入 $\alpha_j, \beta_{ij}$ 来自子问题 `DP1`；其中 `DP1` 是一个线性规划问题，它的输 $y_i$ 来自主问题 `IP3`。问题来了，初始值怎么来。

### 初始化

令 $F_0=\emptyset$。那么主问题就是

{{<katex>}}
$$
\begin{aligned}
\min ~  & \sum_{i=1}^m f_iy_i + z\\[6pt]
\text{s.t. } &y_{i} \in \set{0,1}, ~ z\geq0\quad \forall i
\end{aligned}
$$
{{</katex>}}

其中 $f_i \geq 0$ 设施的开设成本。可以直接看出来，最优解是 $y_i=0, \forall i$。把它代入子问题，我们得到

{{<katex>}}
$$
\begin{aligned}
\max ~  & \sum_{j=1}^n \alpha_j \\[6pt]
\text{s.t. } & \alpha_j -\beta_{ij} \leq c_{ij}, \quad \forall i,j\\[6pt]
& \beta_{ij} \geq 0, \quad \forall i, j
\end{aligned}
$$
{{</katex>}}

如果令 $\alpha_j = \alpha_{ij}, \forall i$，那么约束条件满足。再令 $\alpha_j = \infty$，那么子问题的最优目标函数值是 $\infty$。也就是说，它没有最优解。这就违背了我们之前的假设。

我们需要保证对偶问题 `DP1` 和它的原问题 `LP1` 始终存在最优解。因此，初始化的时候还需要保证子问题的有最优解。注意 `LP1` 是有界的，只要保证它可行，因此 `LP1` 就存在最优解。根那么对偶问题就存在最优解。

根据这样的观察，可以在原问题中加入一个约束条件。

$$
\sum_{j=1}^n y_j \geq 1
$$

它表示至少开设一个设施。那么 `LP1` 始终是可行的，因而有最优解。这也意味着对偶问题 `DP1` 存在最优解。

因此，初始化的时候，考虑如下问题。

{{<katex>}}
$$
\begin{aligned}
\min ~  & \sum_{i=1}^m f_iy_i + z\\[6pt]
\text{s.t. } & \sum_{j=1}^n y_j \geq 1\\
& y_{i} \in \set{0,1}, ~ z\geq0\quad \forall i
\end{aligned}
$$
{{</katex>}}

求解得到初始的 $y$ 值。接下来就可以迭代了。

## 迭代过程

已知初始 $y$ 值，就可以求解子问题。它的最优解记作 $\alpha^1, \beta^1$。在主问题中，它对应的约束就是

$$
\sum_{j=1}^n \alpha_j^1 - \sum_{i=1}^m\sum_{j=1}^n y_i \beta_{ij}^1 \leq z
$$

把约束加入到主问题中。

{{<katex>}}
$$
\begin{aligned}
\min ~  & \sum_{i=1}^m f_iy_i + z\\[6pt]
\text{s.t. } & \sum_{j=1}^n y_j \geq 1\\
& \sum_{j=1}^n \alpha_j^1 - \sum_{i=1}^m\sum_{j=1}^n y_i \beta_{ij}^1 \leq z\\
&y_{i} \in \set{0,1},~ z\geq0 \quad \forall i
\end{aligned}
$$
{{</katex>}}

求解这个问题，从而更新 $y$。这就完成了第一次迭代。

接下来求解子问题，得到最优解 $\alpha^1, \beta^1$。再把对应的约束加入主问题中。

{{<katex>}}
$$
\begin{aligned}
\min ~  & \sum_{i=1}^m f_iy_i + z\\[6pt]
\text{s.t. } 
& \sum_{j=1}^n y_j \geq 1\\
& \sum_{j=1}^n \alpha_j^1 - \sum_{i=1}^m\sum_{j=1}^n y_i \beta_{ij}^1 \leq z\\
& \sum_{j=1}^n \alpha_j^2 - \sum_{i=1}^m\sum_{j=1}^n y_i \beta_{ij}^2 \leq z\\
&y_{i} \in \set{0,1},~ z\geq0 \quad \forall i
\end{aligned}
$$
{{</katex>}}

求解这个问题，然后更新 $y$。这就是第二次迭代。依此类推，直到满足停止条件。

### 停止条件

令 `OPT` 代表原问题的最优目标函数值。令 `OPT_M` 代表主问题的最优目标函数值。我们知道 `OPT_M` 是 `OPT` 的下界，即 `LB := OPT_M ≤ OPT`。

令 `OPT_S` 代表子问题的最优目标函数值。接下来我们找一个最优目标函数值的上界 `UB`。

令 $y^*$ 代表当前步骤主问题的最优解，我们有

{{<katex>}}
$$
\begin{aligned}
OPT & = \min \left\{\sum_{i=1}^m f_i y_i + \max z \right\} \\
& \leq \sum_{i=1}^m f_i y_i^*  + OPT_S = UB
\end{aligned}
$$
{{</katex>}}

我们有

$$
LB \leq \text{OPT} \leq UB
$$

可以证明，随着迭代的进行，下界 `LB` 逐渐增大，上界 `UB` 的值逐渐变小。当上界和下界足够接近时，它们约等于最优目标函数值。

令 $\epsilon > 0$ 表示充分小的数。当 $UB - LB \leq \epsilon $ 时，则停止迭代。

### 最优解

停止迭代后，我们得到了主问题的解 $y, z$，以及子问题的解 $\alpha,\beta$。如何得到原问题的解 $x, y$ 呢。

由于 `DP1` 与 `LP1` 是等价的。 可以把 $y$ 值代入 `LP1` 然后求解得到 $x$。

在实际中，不用这样做。如果把 `DP1` 看成原问题，那么 `LP1` 就是它的对偶问题，$x$ 就是对偶变量。线性规划求解器可以直接返回对偶变量的值。

### 算法描述

**第 0 步，初始化**

初始化主问题并求解。

{{<katex>}}
$$
\begin{aligned}
\min ~ &  \sum_{i=1}^m f_i y_i + z\\
& \sum_{j=1}^n y_j \geq 1\\
& y_j \in \set{0,1}, ~z\geq 0 \quad \forall j
\end{aligned}
$$
{{</katex>}}

令 `UB = INF`。计算  `LB`，它是主问题的最优目标函数值。

**第 1 步，求解子问题**

求解下面的问题。

{{<katex>}}
$$
\begin{aligned}
\max ~  & \sum_{j=1}^n \alpha_j - \sum_{i=1}^m \sum_{j=1}^n \textcolor{blue}{y_i} \beta_{ij}\\[6pt]
\text{s.t. } & \alpha_j -\beta_{ij} \leq c_{ij}, \quad \forall i,j\\[6pt]
& \beta_{ij} \geq 0, \quad \forall i, j
\end{aligned}
$$
{{</katex>}}

其中 $y$ 是输入参数，来自主问题的解。最优目标函数值记作 `OPT_S`。

更新上界 `UB`。

$$
UB = \sum_{i=1}^m f_i y_i + OPT_S
$$

**第 2 步，添加约束**

先判断最优条件。如果 `UB - LB < 1e-6`，则停止并返回最优解。

否则把下面的约束条件添加到主问题中。

$$
\sum_{j=1}^n \textcolor{blue}{\alpha_j} - \sum_{i=1}^m\sum_{j=1}^n y_i \textcolor{blue}{\beta_{ij}} \leq z
$$

其中 $y_i$ 和 $z$ 是变量， $\alpha_j, \beta_{ij}$ 是系数，来自第 1 步中子问题的最优解。


**第 3 步，求解主问题**

求解主问题并更新下界 `LB` 值。

执行 **第 1 步**。

---
weight: 630
title: "整数规划建模技巧"
description: ""
icon: "article"
date: "2025-04-11T13:08:10+08:00"
lastmod: "2025-04-11T13:08:10+08:00"
draft: false
toc: true
katex: true
---

介绍整数规划中的两个约束处理技巧。

### 或约束

下面两个约束至少有一个成立。

{{<katex>}}
$$
\sum_j a_{1j} x_j \leq b_1 \text{ \textcolor{red}{or} }
\sum_j a_{2j} x_j \leq b_2  
$$
{{</katex>}}

这种情况下，不能直接把两个约束写进规划，需要做一些处理。

引入新的变量 {{<katex>}}$y\in \{0,1\}${{</katex>}}，以及非常大的常量 $M$。考虑如下两个约束。

{{<katex>}}
$$
\begin{aligned}
& \sum_j a_{1j} x_j \leq b_1 + My\\
& \sum_j a_{2j} x_j \leq b_2 + M(1-y)
\end{aligned}
$$
{{</katex>}}

如果 $y=0$，第一个不等式就是原问题的第一个约束。

此时第二个不等式为

$$
\sum_j a_{2j} x_j \leq b_2 + M
$$

由于 $M$ 非常大，可以保证它成立。这相当于原问题的第二个约束无效。

如果 $y=1$，第二不等式就是原问题的第二个约束。同理，此时第一个不等式也成立，这相当于原问题的第一个约束无效。

综上，无论那种情况，原来的约束条件中，至少有一个是有效的。


### 条件约束

考虑这样的 `IF - THEN` 这样的条件约束。

$$
\sum_j a_{1j} x_j \leq b_1 \Rightarrow \sum_j a_{2j}x_j \leq b_2
$$

它等价于 

$$
\sum_j a_{1j} x_j > b_1 \text{ \textcolor{red}{or} } \sum_j a_{2j}x_j \leq b_2
$$

严格不等式不能直接在线性规划中做计算。因此引入一个非常小的常数 $\epsilon > 0$，那么上面的条件可以等价地写成

$$
\sum_j a_{1j} x_j \geq b_1 +\epsilon ~\text{ \textcolor{red}{or} } \sum_j a_{2j}x_j \leq b_2
$$

接下来就可以用上面「或」的方法。

引入新的变量 {{<katex>}}$y \in \{0,1\}${{</katex>}}，以及一个非常大的常数 $M$。

考虑下面两个不等式。

{{<katex>}}
$$
\begin{aligned}
& \sum_j a_{1j} x_j \geq b_1 + \epsilon - My\\
& \sum_j a_{2j} \leq b_2 + M (1-y)
\end{aligned}
$$
{{</katex>}}

当 $y=1$ 时，第二个条件 $\sum_j a_{2j} \leq b_2$ 起作用。

当 $y=0$ 时，第一个条件 $\sum_j a_{1j} x_j \geq b_1 + \epsilon$ 起作用。


---
weight: 20
title: "可行区域"
description: ""
icon: "article"
date: "2025-03-24T17:21:06+08:00"
lastmod: "2025-03-24T17:21:06+08:00"
draft: true
toc: true
---



## 几何理解

下面我们从几何的角度来理解线性规划问题。

线性规划问题的约束由 $m$ 个等式定义。从几何上看，每个等式代表一个超平面。$m$ 个超平面相交构成了一个多面体（Polyhedron）。

在三维空间中，如下图所示。

![](https://i-blog.csdnimg.cn/blog_migrate/f604149f337a141fd0ee3ba8c8a0fa9d.jpeg#pic_center)

注意，这个多面体是凸凸的。

作为对比，下面这个多面体就不是凸的：

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b09280cadd1470780b97b09e8bb5e8cb.jpeg#pic_center)


求解线性规划问题，就是要在一个凸多面体 $P$​ 中找到一个点 $x$​，使得目标函数 $c^Tx$​ 最小。

令 $d = c / ||c||$​，把 $d$​ 看成一个超平面 $H$​ 的法向量。注意到$c^Tx =  ||c|| \cdot d^Tx$​，因此最小化 $c^Tx$​ 等价于最小化 $d^Tx$​。

这样一来，线性规划问题可以这样描述：**找一个点 $x\in P$​，离超平面 $H$​ 最近。**

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0aaad6a6916f7b70be2afa28ad2627a8.jpeg#pic_center)


什么点离超平面最近？

**最优解在多面体的顶点上**（证明略）。

有了这样的认知，只要枚举所有顶点，然后看看哪个顶点对应的目标函数值最小，即可找到最优解。但是枚举的效率太低，还有更好的方法，比如单纯形法、内点法。
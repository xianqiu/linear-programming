---
weight: 820
title: "例子"
description: ""
icon: "article"
date: "2025-04-29T15:58:24+08:00"
lastmod: "2025-04-29T15:58:24+08:00"
draft: false
toc: true
katex: true
---

本文介绍一个例子，它叫做 **数独游戏（Sudoku）**。可以用数学规划的方法来求解。以这个例子为背景，我们讲一下如何把模型进行封装，把它作为软件包、网络服务，以及软件产品。

### 数独游戏

我们有一张卡片，它包含  `9*9=81` 个格子，如下图所示。

{{< figure src="sudoku.png" width="320px" class="text-center">}}

卡片上有一些已知的数字，数字的范围是 `1-9`。游戏的任务是，把数字 `1-9` 填入下图的空格子中。填入的数字需要满足如下三个条件。

1. 每行包含数字 `1-9`；
2. 每列包含数字 `1-9`；
3. 每个 **块 (Block)** 包含数字 `1-9`。

解释一下块的概念。每一个块是粗线框包含的 `3*3` 格子。整个表格共有 `9` 个块，分为三行和三列。为了方便描述，我们用记号 `Block(i,j)` 表示位置在第 `i` 行第 `j` 列的块。

`Block(1,1)`

{{< figure src="block11.png" width="100px" class="text-center">}}	

`Block(1,2)`

{{< figure src="block12.png" width="100px" class="text-center">}}	

`Block(1,3)`

{{< figure src="block13.png" width="100px" class="text-center">}}	

依此类推。



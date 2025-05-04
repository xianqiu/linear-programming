---
weight: 840
title: "服务"
description: ""
icon: "article"
date: "2025-04-29T20:51:57+08:00"
lastmod: "2025-04-29T20:51:57+08:00"
draft: false
toc: true
---

在前面的章节中，我们实现了一个生成和求解数独实例的工具。它是一个 `Python` 语言些的类 `SudokuPuzzle` 。这个类有两个方法：`SudokuPuzzle.genearate` 用来生成数独实例，`SudokuSolver.solve` 用来求解数独实例。

我们可以这样使用。

```python
if __name__ == "__main__":
    board = SudokuPuzzle.generate()
    print("\n** Sudoku Puzzle **\n", board)
    solution = SudokuPuzzle.solve(board)
    print("\n** Sudoku Solution **\n", solution)
```

接下来我们把 `SudokuPuzzle` 封装成一个网络服务。这样一来，用户可以通过调用网络服务的方式来使用它的 `generate` 和 `solve` 功能。

为了简化开发，我们需要用到基于 `Python` 的 `Web` 框架。这里我们使用 [FastAPI](https://fastapi.tiangolo.com/tutorial/first-steps/)。用其他框架也可以，比如 `Tornado, Flask` 等。

如下所示。`app` 就是网络服务的实例。运行这段代码，`app` 就会启动。
```python
from fastapi import FastAPI
import uvicorn

# Web Service

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "This is SudokuPuzzle web service."}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

当用户打开浏览器，访问网址 `http://127.0.0.1:8000`，我们就会看到这样的结果。

{{< figure src="index.png" width="400px" class="text-center">}}

处理这个结果的函数就是 `root`；它上面的 `@app.get("/")` 是一个装饰器函数。它的作用是，当用户访问 `http://127.0.0.1:8000` 时，调用 `root`  函数返回请求结果。



接下来把 `SudokuPuzzle` 的两个方法添加到上面的 `app` 中。



定义函数 `generate` 用来返回 `SudokuPuzzle.generate` 的结果，如下所示。

```python
@app.get("/generate")
async def generate():
    board = SudokuPuzzle.genearate()
    return {"board": board.astype(int).tolist()}
```

它上面的装饰器函数 `@app.get("/generate")` 中的参数代表 `URL` 地址。当用户访问 `http://127.0.0.1:8000/generate` 时，它就调用 `generate` 函数，然后把字典转换成 `json` 格式返回。

结果如下图所示。

{{< figure src="generate.png" width="400px" class="text-center">}} 



接下来是求解。由于求解需要输入数独实例。为了让 `FastAPI` 能解析数独实例，需要按照下面的方式定义一个数据结构 `SudokuBoard`。

```python
from pydantic import BaseModel


class SudokuBoard(BaseModel):
    board: list[list[int]]
```

然后定义 `solve` 方法。它调用 `SudokuPuzzle.solve` 求解数独实例，并返回结果。

```python
@app.post("/solve")
async def solve(sudoku: SudokuBoard):
    try:
        board = SudokuPuzzle.solve(sudoku.board)
        if board is not None:
            status = "SOLVED"
    except Exception as e:
        status = "INFEASIBLE"

    return {
        "status": status,
        "solution": board.astype(int).tolist()
    }
```
其中 `@app.post("/solve")` 表示请求方式为 `post`。请求时需要把数据进行封装，然后发送到地址 `http://127.0.0.1:8000/solve`。

下面是请求示例。

```python
def test_solve():
    url = "http://localhost:8000/solve"
    headers = {"Content-Type": "application/json"}
    board = [
        [0, 2, 0, 0, 3, 0, 0, 9, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 7, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 6, 2],
        [5, 0, 0, 0, 6, 0, 0, 0, 0],
        [0, 0, 7, 0, 0, 0, 0, 0, 0],
        [0, 0, 9, 7, 0, 1, 0, 0, 0],
        [0, 4, 0, 0, 0, 0, 0, 2, 0],
        [0, 0, 0, 5, 0, 0, 0, 0, 0]
    ]
    response = requests.post(url, headers=headers, 
                            data=json.dumps({"board": board}))
    content = response.json()
    print(content)
    

if __name__ == '__main__':
    test()
```

总结一下。

通过上面的方式，我们把 `SudokuPuzzle`  封装成了一个本地的在线服务。 接口 `/generate`，可以通过浏览器直接请求，得到一个数独实例；然后把数据封装成 `json` 格式，通过 `post` 方式发送给接口 `/solve`，从而求解这个数独实例。

这样做的好处是，不要求用户会 `python`，只要会使用 `get` 和 `post` 方式发送请求，就可以使用数独生成和求解的功能。利用这个服务，我们还可以给它做一个前端界面。这样一来，即使用户不会编程，也可以使用这两个功能。

最后附上相关代码。

* [codes/application/service/](https://github.com/xianqiu/linear-programming/tree/main/codes/application/service/) 文件夹
	* [sudoku_service.py](https://github.com/xianqiu/linear-programming/tree/main/codes/application/service/sudoku_service.py) 数独实例生成和求解的服务
	* [test_sudoku_service.py](https://github.com/xianqiu/linear-programming/tree/main/codes/application/service/test_sudoku_service.py) 测试代码



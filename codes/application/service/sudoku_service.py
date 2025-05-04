from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

# Need to import the SudokuPuzzle class from the sudoku package
# which is located in the parent directory of the current directory
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent/"sudoku"))
from sudoku import SudokuPuzzle
from fastapi.middleware.cors import CORSMiddleware


# Web Service

app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows specific origins
    allow_credentials=True, # Allows cookies to be sent in cross-origin requests (if needed)
    allow_methods=["*"],    # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],    # Allows all headers
)


@app.get("/")
async def root():
    return {"message": "This is SudokuPuzzle web service."}


@app.get("/generate")
async def generate():
    board = SudokuPuzzle.genearate()
    return {"board": board.astype(int).tolist()}


class SudokuBoard(BaseModel):
    board: list[list[int]]


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


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
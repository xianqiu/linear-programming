from enum import Enum


class Status(Enum):
    OPTIMAL = 1
    UNBOUNDED = 2
    INFESIBLE = 3
    MAX_ITER = 4



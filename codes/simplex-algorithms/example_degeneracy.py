import json
from simplex_basic import SimplexBasic


def solve_instance(instance, index=""):
    A, b, c, s = instance['A'], instance['b'], instance['c'], instance['s']
    print(f"==== instance{index} ====")
    print(f"|-- A: {A}")
    print(f"|-- b: {b}")
    print(f"|-- c: {c}")
    print(f"|-- s: {s}")
    print("------------------------")
    simplex = SimplexBasic(A, b, c, s)
    simplex.max_iter = 10
    simplex.solve()
    print(f"status: {simplex.status}")


def show_degen(index=0):
    # Show degenerate example.
    with open('test-data/degen.json', 'r') as f:
        instances = json.load(f)
    assert 0 <= abs(index) < len(instances), "index out of range"
    solve_instance(instances[index], index)


def show_cycle(index=0):
    # Show degenerate example which yields cycling.
    with open('test-data/cycle.json', 'r') as f:
        instances = json.load(f)
    assert 0 <= abs(index) < len(instances), "index out of range"
    solve_instance(instances[index], index)


if __name__ == '__main__':
    show_degen(0)
    # show_cycle(0)
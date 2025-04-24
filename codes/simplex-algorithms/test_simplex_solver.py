import json

from simplex_solver import SimplexSolver
from common import Status


def test_instance(instance):
    A, b, c = instance['A'], instance['b'], instance['c']
    opt_type = instance.get('opt_type', 'min')
    simplex = SimplexSolver(A, b, c)
    if opt_type == 'max':
        simplex.maximize().solve()
    else:
        simplex.solve()
    
    expected = instance['opt']
    if expected == "-inf" or expected == "inf":
        assert simplex.status == Status.UNBOUNDED, f"Test Failed. Instance = {instance}"
    elif expected == None:
        assert simplex.status == Status.INFEASIBLE, f"Test Failed. Instance = {instance}"
    else:
        
        assert abs(simplex.objective - expected) < 1e-6, f"Test Failed. Instance = {instance}"


def test_file(filename):
    with open(filename, 'r') as f:
        instances = json.load(f)
    for instance in instances:
        test_instance(instance)
    print(f"[Test Passed] Count = {len(instances)}, Filename = {filename}")


def tests():
    from pathlib import Path
    directory = Path(__file__).parent / 'test-data'
    filenames = [
        "solver.json",
        "twophase.json",
        "degen.json",
        "cycle.json"
    ]
    for filename in filenames:
        test_file(directory / filename)


if __name__ == '__main__':
    tests()
    
    
    
import json

from simplex_twophase import SimplexTwoPhase
from common import Status


def test_instance(instance):
    A, b, c = instance['A'], instance['b'], instance['c']
    simplex = SimplexTwoPhase(A, b, c)
    simplex.print_info = False
    simplex.solve()
    expected = instance['opt']
    if expected == "-inf":
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
    filenames = [
        "test-data/twophase.json",
        "test-data/degen.json",
        "test-data/cycle.json"
    ]
    for filename in filenames:
        test_file(filename)


if __name__ == '__main__':
    tests()
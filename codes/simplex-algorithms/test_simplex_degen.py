import json

from common import Status
from simplex_degen import SimplexDegen


def test_instance(instance):
    A, b, c, s = instance['A'], instance['b'], instance['c'], instance['s']
    simplex = SimplexDegen(A, b, c, s)
    simplex.print_iter = False
    simplex.max_iter = 20
    simplex.solve()
    expected = instance['opt']
    if expected == "-inf":
        assert simplex.status == Status.UNBOUNDED, f"Test Failed. Instance = {instance}"
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
        "test-data/degen.json",
        "test-data/cycle.json"
    ]
    for filename in filenames:
        test_file(filename)


if __name__ == '__main__':
    tests()
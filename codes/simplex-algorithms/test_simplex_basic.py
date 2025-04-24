from simplex_basic import SimplexBasic
from common import Status
import json


def test_instance(instance):
    A, b, c, s = instance['A'], instance['b'], instance['c'], instance['s']
    simplex = SimplexBasic(A, b, c, s)
    simplex.print_iter = False
    simplex.solve()
    expected = instance['opt']
    if expected == "-inf":
        assert simplex.status == Status.UNBOUNDED, f"Test Failed. Instance = {instance}"
    else:
        assert abs(simplex.objective - expected) < 1e-6, f"Test Failed. Instance = {instance}"


def tests():
    from pathlib import Path
    directory = Path(__file__).parent / 'test-data'
    filename = 'basic.json'
    with open(directory / filename, 'r') as f:
        instances = json.load(f)
    for instance in instances:
        test_instance(instance)
    print(f"[Test Passed] Count = {len(instances)}, Filename = {filename}")


if __name__ == '__main__':
    tests()
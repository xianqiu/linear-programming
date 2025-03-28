from simplex_basic import SimplexBasic
from common import Status
import json


def load_instances(filename):
    filename = 'test-data/basic.json'
    with open(filename, 'r') as f:
        instances = json.load(f)
    return instances


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
    instances = load_instances('test-data/basic.json')
    for instance in instances:
        test_instance(instance)
    print(f"[Test Passed] {len(instances)} instances.")


if __name__ == '__main__':
    tests()
    
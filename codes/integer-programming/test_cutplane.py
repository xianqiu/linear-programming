import json

from cutplane import CutPlane


def test_instance(instance):
    A, b, c = instance['A'], instance['b'], instance['c']
    cp = CutPlane(A, b, c)
    cp.print_info = False
    cp.solve()
    expected = instance['opt']
    if expected == "inf":
        assert cp.status == "UNBOUNDED", f"Test Failed. Instance = {instance}"
    elif expected == None:
        assert cp.status == "INFEASIBLE", f"Test Failed. Instance = {instance}"
    else:
        assert abs(cp.objective - expected) < 1e-6, f"Test Failed. Instance = {instance}"


def tests():
    from pathlib import Path
    directory = Path(__file__).parent
    filename = 'integer.json'
    with open(directory / filename, 'r') as f:
        instances = json.load(f)
    for instance in instances:
        test_instance(instance)
    print(f"[Test Passed] Count = {len(instances)}, Filename = {filename}")


if __name__ == '__main__':
    tests()
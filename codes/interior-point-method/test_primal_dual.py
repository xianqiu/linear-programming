import json

from primal_dual import PDInteriorPoint


def test_instance(instance):
    A, b, c = instance['A'], instance['b'], instance['c']
    pd = PDInteriorPoint(A, b, c)
    pd.print_iter = False
    pd.solve()
    expected = instance['opt']
    assert abs(pd.objective - expected) < 1e-6, f"Test Failed. Instance = {instance}"


def tests():
    from pathlib import Path
    directory = Path(__file__).parent
    filename = 'interior.json'
    with open(directory / filename, 'r') as f:
        instances = json.load(f)
    for instance in instances:
        test_instance(instance)
    print(f"[Test Passed] Count = {len(instances)}, Filename = {filename}")


if __name__ == '__main__':
    tests()
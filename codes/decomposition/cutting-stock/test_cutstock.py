import numpy as np

from exact import CutStockExact
from approximate import CutStockApprox
from column_generation import CutStockApproxCG


class RandomInstance:

    def __init__(self, m):
        """
        m: number of stock sizes
        """
        self.L = 1000
        self.s = np.random.randint(100, 500, m)
        self.d = np.random.randint(100, 1000, m)

    def size(self):
        """ Estimate the instance size, i.e.
        the number of feasible cuts.
        """
        ub = (self.L // np.array(self.s)).astype(int)
        return np.prod(ub)


class TestCutStock:

    """ Test cutting stock algorithms.
    """

    timeout = 60  # in seconds
    print_info = True

    methods = [
        CutStockExact,
        CutStockApprox,
        CutStockApproxCG
    ]

    def __init__(self, m):
        """
        m: number of stock sizes
        """
        self.ins = RandomInstance(m)
        self.L = self.ins.L
        self.s = self.ins.s
        self.d = self.ins.d

    def _run_method(self, Method):
        algorithm = Method(self.L, self.s, self.d)
        algorithm.timeout = self.timeout
        algorithm.solve()
        return algorithm

    def _check(self, algorithm):
        # s^Tx <= L
        cuts = np.array(algorithm.cuts)
        s = np.array(self.ins.s)
        assert np.all(s @ cuts <= algorithm.L), "Infeasible cuts."
        # Ax >= d
        x = np.array(algorithm.x)
        cuts = np.array(algorithm.cuts)
        d = np.array(self.ins.d)
        assert np.all(cuts @ x >= d), "Infeasible. Not all demands are satisfied."
        # objective
        assert algorithm.count == sum(algorithm.x), "Wrong objective."
        
    def test(self):
        for method in self.methods:
            algorithm = self._run_method(method)
            self._check(algorithm)


class TestCutStockBatch:

    m = 6  # number of stock sizes
    b = 100  # number of instances
    timeout = 1  # in seconds
    
    @classmethod
    def test(cls):
        print("-" * 50)
        print("Testing.")
        for i in range(1, cls.b+1):
            print(f">> Instance: {i}/{cls.b}")
            t = TestCutStock(cls.m)
            t.timeout = cls.timeout
            t.test()
        print(">> [Test] passed.")
            

if __name__ == "__main__":
    TestCutStockBatch.test()

    
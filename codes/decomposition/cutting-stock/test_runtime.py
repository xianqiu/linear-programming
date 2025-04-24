import time

import numpy as np

from exact import CutStockExact
from approximate import CutStockApprox
from column_generation import CutStockApproxCG

from test_cutstock import RandomInstance


class TestRunTime:

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
        start = time.time()
        cs = Method(self.L, self.s, self.d)
        cs.timeout = self.timeout
        objective = cs.solve().count
        elapsed_time = time.time() - start

        return  {
            "method": Method.__name__,
            "objective": objective,
            "elapsed_time": elapsed_time,
            "status": cs.status
        }

    def _print_result(self, result, enable=True):
        if not enable:
            return
        print("-" * 50)
        print(f"Method: {result['method']}")
        print(f"|-- Elapsed time: {result['elapsed_time']:.2f} seconds")
        print(f"|-- Objective: {result['objective']}")
        print(f"|-- Status: {result['status']}")

    def _print_instance(self, enable=True):
        if not enable:
            return
        print("-" * 50)
        print(f"Instance: k={len(self.s)}")
        print(f"|-- L: {self.L}")
        print(f"|-- s: {self.s}")
        print(f"|-- d: {self.d}")
        print(f"|-- Timeout: {self.timeout} seconds")
        print(f"|-- Size of columns: {self.ins.size()}")

    def run(self):
    
        self._print_instance(self.print_info)
        results = []
        for method in self.methods:
            result = self._run_method(method)
            results.append(result)
            self._print_result(result, self.print_info)

        return results


class TestRunTimeBatch:

    def __init__(self, m, b, timeout):
        """
        m: number of stock sizes
        b: number of instances
        timeout: timeout in seconds
        """
        self.m = m
        self.b = b
        self.timeout = timeout
        self.records = None

    def _print_header(self):
        print("-" * 50)
        print(f"Running multiple instances.")
        print(f"|-- Instances number = {self.b}")
        print(f"|-- Stock sizes number = {self.m}")
        print(f"|-- Instance size = {RandomInstance(self.m).size()}")
        print(f"|-- Timeout = {self.timeout} seconds")
        print(f"|-- Methods: {[m.__name__ for m in TestRunTime.methods]}")
        print("-" * 50)
    
    def run(self):
        self._print_header()
        results = []
        for i in range(self.b):
            t = TestRunTime(self.m)
            print(f">> Instance {i+1}/{self.b}")
            print(f"   |-- L = {t.L}, s = {t.s}, d = {t.d}")
            t.timeout = self.timeout
            t.print_info = False
            result = t.run()
            results.append(result)
        self.records = self._format(results)
        self.statistics()

        return self

    def _format(self, results):
        """
        Format results into a dictionary.
        """
        records = {}
        for result in results:
            for r in result:
                if r["method"] not in records:
                    records[r["method"]] = {
                        "objective": [],
                        "elapsed_time": [],
                        "status": []
                    }
                records[r["method"]]["objective"].append(r["objective"])
                records[r["method"]]["elapsed_time"].append(r["elapsed_time"])
                records[r["method"]]["status"].append(r["status"])
        return records

    def statistics(self):
        """
        Calculate the statistics of the results.
        """
        if self.records is None:
            return 

        stats = {}
        for method in self.records:
            status_list = self.records[method]["status"]
            item = {
                "solved_number": sum(1 for status in status_list if "OPTIMAL" in status),
                "mean_elapsed_time": np.mean(self.records[method]["elapsed_time"])
            }
            stats[method] = item

        return stats

    def print_statistics(self):
        """
        Print the statistics of the results.
        """
        if self.records is None:
            return
        stats = self.statistics()
        print("-" * 50)
        print(f"Statistics:")
        for method in stats:
            print(f"|-- Method: {method}")
            print(f"    |-- Solved number: {stats[method]['solved_number']}")
            print(f"    |-- Mean elapsed time: {stats[method]['mean_elapsed_time']:.2f} seconds")
        print("-" * 50)
    

def estimate_instance_sizes():
    print(f"Estimated instance sizes")
    for m in range(5, 21):
        # estimate in multiple times and take the average
        sizes = np.array([RandomInstance(m).size() for _ in range(100)])
        size = np.mean(sizes).astype(int)
        print(f">> m = {m}, size = {size}")
        

def solve_small_instances():
    """
    Compare the three methods on small instances.
    """
    t = TestRunTimeBatch(m=8, b=100, timeout=1)
    t.run().print_statistics()
 

def solve_large_instances():
    """ Use column generation method to solve large instances.
    As direct methods cannot solve them.
    """
    t = TestRunTimeBatch(m=20, b=100, timeout=10)
    TestRunTime.methods = [CutStockApproxCG]
    t.run().print_statistics()


if __name__ == "__main__":
    estimate_instance_sizes()
    # solve_small_instances()
    # solve_large_instances()

    
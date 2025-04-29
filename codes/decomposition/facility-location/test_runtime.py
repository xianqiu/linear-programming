import time

import numpy as np

from exact import FacilityLocationExact
from benders import FacilityLocationBenders


class RandomInstance:

    def __init__(self, m, n):
        """
        m: number of facility locations
        n: number of customers
        """
        self.f = np.random.randint(10, 100, m)
        self.C = np.random.randint(1, 20, (m, n))


class TestRunTime:

    timeout = 30  # seconds
    print_info = True

    methods = [
        FacilityLocationExact,
        FacilityLocationBenders
    ]

    def __init__(self, m, n):
        """
        m: number of facility locations
        n: number of customers
        """
        self.ins = RandomInstance(m, n)
        self.f = self.ins.f
        self.C = self.ins.C

    def _run_method(self, Method):
        start = time.time()
        fl = Method(self.f, self.C)
        fl.print_info = False
        fl.timeout = self.timeout
        objective = fl.solve().objective
        elapsed_time = time.time() - start

        return  {
            "method": Method.__name__,
            "objective": objective,
            "elapsed_time": elapsed_time,
            "status": fl.status
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
        m, n = self.C.shape
        print(f"Instance: m = {m}, n = {n}")
        print(f"|-- Time Limit: {self.timeout} seconds")

    def run(self):
    
        self._print_instance(self.print_info)
        results = []
        for method in self.methods:
            result = self._run_method(method)
            results.append(result)
            self._print_result(result, self.print_info)

        return results


class TestRunTimeBatch:

    def __init__(self, m, n, b, timeout):
        """
        m: number of facility locations
        n: number of customers
        b: number of instances
        timeout: timeout in seconds
        """
        self.m = m
        self.n = n
        self.b = b
        self.timeout = timeout
        self.records = None

    def _print_header(self):
        print("-" * 50)
        print(f"Running multiple instances.")
        print(f"|-- Instance number = {self.b}")
        print(f"|-- Facility location number = {self.m}")
        print(f"|-- Customer number = {self.n}")
        print(f"|-- Time limit = {self.timeout} seconds")
        print(f"|-- Methods: {[m.__name__ for m in TestRunTime.methods]}")
        print("-" * 50)
    
    def run(self):
        self._print_header()
        results = []
        for i in range(self.b):
            t = TestRunTime(self.m, self.n)
            print(f">> Instance {i+1}/{self.b}")
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


def test_small():
    t = TestRunTimeBatch(m=20, n=100, b=100, timeout=5)
    t.run().print_statistics()


def _solve_instance(ins, Method, timeout):
    print("-" * 50)
    print(f">> [Solving] Method = {Method.__name__}")
    start = time.time()
    fl = Method(ins.f, ins.C)
    fl.timeout = timeout
    fl.solve()
    print(f">> [Done] {fl.status}")
    print(f"Elapsed time: {time.time() - start:.2f} seconds")
    print(f"Objective: {fl.objective}")


def test_large():
    r = RandomInstance(m=50, n=6000)
    methods = [
        #FacilityLocationExact,
        FacilityLocationBenders
    ]
    for method in methods:
        _solve_instance(r, method, timeout=30)


if __name__ == '__main__':
    test_small()
    # test_large()


    


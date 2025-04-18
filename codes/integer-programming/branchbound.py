from ortools.linear_solver import pywraplp
import numpy as np


class Node(object):

    """ Linear Program (LP) instance.
    
    The instance is defined as:
            max c^T x
            s.t. Ax <= b
                 x >= 0
        where:
            c: n-dim vector
            A: m x n matrix
            b: m-dim vecto
    """

    def __init__(self, A, b, c):
        self.A = A
        self.b = b
        self.c = c
        self.solution = None
        self.objective = None


class LPSolver:

    """ Use ortools to solve a linear program instance.
        The instance is defined as:
            max c^T x
            s.t. Ax <= b
                 x >= 0
        where:
            c: n-dim vector
            A: m x n matrix
            b: m-dim vecto
        The solution is stored in the node.
    """

    def __init__(self, node):
        """
        Args:
            node: Node object, The LP instance.
        """
        self.node = node
        self.status = None

    def solve(self):
        """ Solve the instance.
        """
        # Create the linear solver with the CLP backend.
        # DO NOT use GLOP, which does not recongize UNBOUNDED case.
        s = pywraplp.Solver.CreateSolver('CLP')
        # Decision variables.
        n = len(self.node.c)
        x = [s.NumVar(0, s.infinity(), f"x-{j}") for j in range(n)]
        # Constraints: Ax <= b
        m = len(self.node.b)
        for i in range(m):
            ct = s.Constraint(-s.infinity(), self.node.b[i], f"ct-{i}")
            for j in range(n):
                ct.SetCoefficient(x[j], self.node.A[i][j])
        # Objective function
        obj = s.Objective()
        for j in range(n):
            obj.SetCoefficient(x[j], self.node.c[j])
        obj.SetMaximization()
        # Solve
        self.status = s.Solve()
        if self.status == s.OPTIMAL:
            self.node.solution = [x[j].solution_value() for j in range(n)]
            self.node.objective = obj.Value()
            
        return self


class BranchAndBound:
    
    """ Branch and bound algorithm.
    """

    print_info = True
    max_visited = 1_000
    
    def __init__(self, A, b, c):
        """
        Args:
            c: n-dim vector
            A: m x n matrix
            b: m-dim vector
        """
        self.A = A
        self.b = b
        self.c = c
        self.root = Node(A, b, c)
        # Best search result
        self._best_solution = None
        self._best_objective = -np.inf
        self._count = 0  # Count the number of visited nodes
        # Final Solution
        self.solution = None
        self.objective = None
        self.status = None

    def _is_feasible(self, solution):
        """ Check if the solution is integer solution.
        """
        for x in solution:
            if not np.isclose(x, np.round(x)):
                return False
        return True

    def _branch(self, node):
        """ Branch the node.
        """
        # x[j] is not integer, branch on x[j]
        j = np.argmax(np.abs(np.array(node.solution) - np.round(node.solution)))
        b0 = np.floor(node.solution[j])
        
        # Node1
        # Add constraint: x[j] <= b0
        b1 = np.concatenate((node.b, np.array([b0])), axis=0)
        a1 = np.zeros(len(node.c))
        a1[j] = 1
        A1 = np.concatenate((node.A, a1.reshape(1, -1)), axis=0)
        node1 = Node(A1, b1, node.c)

        # Node2
        # Add constraint: x[j] >= b0 + 1  <=> -x[j] <= -b0 - 1
        b2 = np.concatenate((node.b, np.array([-b0-1])), axis=0)
        a2 = np.zeros(len(node.c))
        a2[j] = -1
        A2 = np.concatenate((node.A, a2.reshape(1, -1)), axis=0)
        node2 = Node(A2, b2, node.c)
        
        return node1, node2


    def _search(self, node):
        """ Depth first search.
        """
        # Solve the LP instance
        self.status = LPSolver(node).solve().status

        self._count += 1
        if self._count == self.max_visited:
            self.status = pywraplp.Solver.FEASIBLE
            return

        if self.status != pywraplp.Solver.OPTIMAL:
            # Return if not optimal
            # E.g. infeasible, unbounded, unknown
            return

        # Print the node
        self._print_node(node, self.print_info)
        
        # Prune
        if node.objective < self._best_objective:
            return
        # Integer solution
        if self._is_feasible(node.solution):
            # Update the best solution
            if node.objective > self._best_objective:
                self._best_solution = node.solution
                self._best_objective = node.objective
            return
        
        # Branch
        node1, node2 = self._branch(node)
        self._print_branch(node1, self.print_info)
        self._print_branch(node2, self.print_info)
        # Search
        self._search(node1)
        self._search(node2)

    def _print_branch(self, node, enable=True):
        """ Print the branch.
        """
        if not enable:
            return
        j = np.nonzero(node.A[-1, :])[0][0]
        b = node.b[-1]
        if b > 0:
            print(f'>> branch at: x[{j}] <= {int(b)}')
        else:
            print(f'>> branch at: x[{j}] >= {-int(b)}')

    def _print_node(self, node, enable=True):
        """ Print the node.
        """
        if not enable:
            return
        print(f'>> Solve node:')
        print(f'   |-- A: {node.A}')
        print(f'   |-- b: {node.b}')
        print(f'   |-- c: {node.c}')
        print(f'   |-- solution: {node.solution}')
        print(f'   |-- objective: {node.objective}')

    def solve(self):
        """ Solve the problem.
        """
        self._search(self.root)
        
        if self._best_solution is not None:
            self.status = 'OPTIMAL'
            self.solution = self._best_solution
            self.objective = self._best_objective
        elif self.status == pywraplp.Solver.UNBOUNDED:
            self.status = 'UNBOUNDED'
            self.objective = np.inf
        elif self.status == pywraplp.Solver.INFEASIBLE:
            self.status = 'INFEASIBLE'
        else:
            self.status = 'UNKNOWN'


if __name__ == '__main__':

    A = [[1, 4], [3, -4]]
    b = [10, 6]
    c = [4, 5]
 
    solver = BranchAndBound(A, b, c)
    solver.solve()
    print("-"*20)
    print(f"Solution: {solver.solution}")
    print(f"Objective: {solver.objective}")
    print(f"Status: {solver.status}")
    
    
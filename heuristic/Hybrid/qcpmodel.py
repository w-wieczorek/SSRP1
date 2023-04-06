import sys
import gurobipy as gp
from gurobipy import GRB
from collections import namedtuple
import numpy as np

InputData = namedtuple("InputData", "n m k sigma words")
Result = namedtuple("Result", "optimal x_vals")

def BuildAndSolve(time_limit: int, data: InputData) -> Result:
    try:
        model = gp.Model("qcp.log")
        model.Params.NonConvex = 2
        model.Params.TimeLimit = time_limit
        model.Params.Threads = 1
        i: int 
        j: int
        x = model.addMVar(shape=data.n, vtype=GRB.BINARY , name="x")
        y = model.addMVar(shape=data.m, vtype=GRB.BINARY , name="y")
        z = model.addMVar((data.m, len(data.sigma)), vtype=GRB.BINARY, name="z")
        model.addConstr(y.sum() == data.m - data.k, "cy")
        for j in range(data.m):
            model.addConstr(sum(z[j, a] for a in range(len(data.sigma))) == 1, f"c{j}")
        qexp: gp.QuadExpr = 0
        for i in range(data.n):
            qexp = 0
            for j in range(data.m):
                qexp += y[j] * z[j, data.sigma.index(data.words[i][j])]
            model.addConstr(qexp >= (data.m - data.k) * x[i], f"q{i}")
        model.setObjective(x.sum(), GRB.MAXIMIZE)
        model.optimize()
        is_optimal: bool
        vals = []
        if model.Status == GRB.OPTIMAL:
            is_optimal = True
            print("Optimal solution found by QCP.")
        else:
            is_optimal = False
        solution = np.zeros(data.n)        
        for i in range(data.n):
            if x.X[i] > 0.5:
                solution[i] = 1.0
        return Result(is_optimal, solution)
    except gp.GurobiError as e:
        sys.exit('Error code ' + str(e. errno ) + ": " + str(e))

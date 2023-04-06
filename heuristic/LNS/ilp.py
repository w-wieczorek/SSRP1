from typing import List

from docplex.mp.model import Model


def find_solution(input: List[str], k: int, fixed_words: List[str] = [], t_max=15, log_output: bool = True) -> List[str]:
    mdl = Model('SSRP')

    s = [' ']+[' ' + word for word in input] # i, j are indexed from one not from zero

    n = len(input)
    N = [i for i in range(1, n+1)]

    m = len(input[0])
    M = [j for j in range(1, m+1)]

    Alphabet = {s[i][j] for i in N for j in M}

    Z = [(j, a) for j in M for a in Alphabet]

    Sigma = {j: {s[i][j] for i in N} for j in M} # Sigma_j

    x = mdl.binary_var_dict(N, name='x') # variables (5)
    z = mdl.binary_var_dict(Z, name='z') # variables (6)
    y = mdl.binary_var_dict(M, name='y') # variables (7)

    for i in N:
        for j in M:
            mdl.add_constraint(x[i] <= z[j, s[i][j]]) # inequalities (2)

    mdl.add_constraints(mdl.sum(z[j, a] for a in Sigma[j]) <= 1 + (len(Sigma[j])-1) * y[j] for j in M) # inequalities (3)

    mdl.add_constraint(mdl.sum(y[j] for j in M) <= k) # inequality (4)

    for w in fixed_words:
        i = input.index(w) + 1 
        mdl.add_constraint(x[i] == 1) # equation (10)

    mdl.maximize(mdl.sum(x[i] for i in N)) # objective (1)
    mdl.parameters.timelimit = t_max
    mdl.context.cplex_parameters.threads = 1
    mdl.solve(log_output=log_output)

    return [input[i-1] for i in N if x[i].solution_value == 1.0]

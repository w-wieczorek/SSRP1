from typing import List
from random import randint, random, choice
from timeit import default_timer as timer

import numpy as np
from mealpy.evolutionary_based.GA import EliteSingleGA

from greedyf import greedy_f
from graph import diff_vector2, get_diff_vector



def init_population(I: List[str], k, pop_size: int, init_solution = None):
    sbsf = greedy_f(I, k)
    idx_hash = {s: i for i, s in enumerate(I)}

    sbsf_init = np.zeros(len(I))
    for s in sbsf:
        sbsf_init[idx_hash[s]] = 1.0
        
    print(f"Init solution: {np.sum(init_solution)}")
    print(f"SBSF solution: {np.sum(sbsf_init)}")

    starting_positions, template_solutions = [sbsf_init], [sbsf_init]     
    if init_solution is not None:
        starting_positions.append(init_solution)
        template_solutions.append(init_solution)        
        
    empty_sol = np.zeros(len(I))
    for _ in range(pop_size-len(starting_positions)):
        ind = choice(template_solutions).copy()
        idxs = np.random.choice(range(0, len(I)), 2, replace=False)
        cut1, cut2 = np.min(idxs), np.max(idxs)
        ind = np.concatenate([ empty_sol[:cut1], ind[cut1:cut2], empty_sol[cut2:] ])
        for _ in range(3):
            ind[randint(0, len(I)-1)] = random() * 2
        starting_positions.append(ind)

    return starting_positions

def run_ga(I: List[str], k: int, time_limit_sec: int, init_solution = None) -> int:
    pop_size = 100
    pc = 0.95
    pm = 0.01
    k_way = 0.2
    mutation = "flip"

    LB = [0] * len(I)
    UB = [1.99] * len(I)

    start = timer()

    diff_vector = get_diff_vector(I)

    def fitness_function(solution):
        solution_int = solution.astype(int)
        curr_k = diff_vector2(diff_vector, solution_int, len(I[0]))

        return 0 if curr_k > k else np.sum(solution_int)    

    starting_positions = init_population(I, k, pop_size, init_solution)

    problem = {
        "fit_func": fitness_function,
        "lb": LB,
        "ub": UB,
        "minmax": "max",
    }

    termination = {
        "mode": "TB",
        "quantity": time_limit_sec - int(timer() - start)
    }

    alg = EliteSingleGA(pop_size=pop_size, 
                       pc=pc, pm=pm, 
                       selection="tournament", 
                       k_way=k_way, 
                       mutation=mutation)
    best_position, best_fitness = alg.solve(problem, starting_positions=starting_positions, termination=termination)
    print(f"Found set: {best_fitness}")
    print(f"Curr k: {diff_vector2(diff_vector, best_position.astype(int), len(I[0]))}")
    print(best_position.astype(int))

    return best_fitness

from typing import List
from itertools import chain

from antsys import AntWorld
from antsys import AntSystem, Edge

from graph import build_graph, has_edge



def read_problem(file_name: str) -> List[str]:
    with open(file_name, 'r') as f:
        return f.readlines()


def main():
    k = 50
    p_panishment = 4
    p_not_included = 2
    p_success = 1

    strings = read_problem('words_500_0500_04_0.025.dat')
    adj_mat = build_graph(strings, k)

    def rules(start, end):
        edge_exists, _ = has_edge(start, end, adj_mat)
        if edge_exists:
            return [0, 1]
        else:
            return [0]

    def cost(path: List[Edge]):
        # return -sum(e.info for e in path)
        # return sum_diff(path)
        diff = sum_diff(path)

        if diff > k:
            return 1000  
        return -sum(e.info for e in path)*2


    def heuristic(path: List[Edge], candidate: Edge):
        if candidate.info == 0:
            return p_not_included
        
        cand_has_edge, _ = has_edge(candidate.start, candidate.end, adj_mat)

        if not cand_has_edge:
            return p_panishment

        path_diff = sum_diff(chain(path, [candidate]))
        
        return p_success if path_diff <= k else p_panishment
                
    def print_solution(g_best: List[Edge]):
        countity = sum(e.info for e in g_best)*2
        sol_diff = sum_diff(g_best)
        print(f"Countity: {countity}, Diff: {sol_diff}, k={k}")

    def sum_diff(path: List[Edge]):
        sol_diff = set()

        for e in path:
            if e.info == 1:
                _, e_diff = has_edge(e.start, e.end, adj_mat)
                sol_diff.update(e_diff)

        return len(sol_diff)

    new_world = AntWorld(list(range(len(strings))), rules, cost, heuristic, False)
    ant_opt = AntSystem(world=new_world, n_ants=25)
    ant_opt.optimize(500, 500)
    print_solution(ant_opt.g_best[2])

main()
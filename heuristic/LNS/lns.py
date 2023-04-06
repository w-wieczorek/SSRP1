from statistics import mean
from timeit import default_timer as timer
import argparse
import logging
from typing import List

from common import destroy_partially
from greedyf import greedy_f
from ilp import find_solution
# from qcp import find_solution


def run_test(I: List[str], k: int, time_limit: int, t_max: int, perc_l: int, perc_u: int) -> List[str]:
    start = timer()              
    perc_l, perc_u = perc_l, perc_u #percentages 0-100         

    # algorithm 3 begins
    Sbsf = greedy_f(I, k)
    perc_dest = perc_l    
    while timer() - start < time_limit:
        Sp = destroy_partially(Sbsf, perc_dest)
        Sopt = find_solution(I, k, Sp, t_max, log_output=True)
        if len(Sopt) > len(Sbsf):
            Sbsf = Sopt
            perc_dest = perc_l
        else:
            perc_dest = perc_dest + 5
            if perc_dest > perc_u:
                perc_dest = perc_l
    return Sbsf


def run_tests(file_name: str, k: int, time_limit: int, t_max: int, perc_l: int, perc_u: int, repeats: int):
    I: List[str] = [l.strip() for l in open(file_name, 'r').readlines()]

    solutions_lengths: List[int] = []

    for _ in range(repeats):
        best_sol = run_test(I, k, time_limit, t_max, perc_l, perc_u)
        solutions_lengths.append(len(best_sol))

    logger = logging.Logger('lns')
    logger.addHandler(logging.FileHandler('log', mode='a'))
    logger.info(f'{file_name}\t{len(I)}\t{len(I[0])}\t{k}\t{time_limit}\t{mean(solutions_lengths)}\t{max(solutions_lengths)}')        


if __name__ == '__main__':
    parser = argparse.ArgumentParser()    
    parser.add_argument("--file", action='store', type=str)
    parser.add_argument("--k", action='store', type=int)
    parser.add_argument("--perc_l", action='store', default=30, type=int)
    parser.add_argument("--perc_u", action='store', default=70, type=int)
    parser.add_argument("--time_limit", action='store', default=30, type=int)
    parser.add_argument("--t_max", action='store', default=15, type=int)
    parser.add_argument("--repeats", action='store', default=30, type=int)
    
    args = parser.parse_args()

    run_tests(args.file, args.k, args.time_limit, args.t_max, args.perc_l, args.perc_u, args.repeats)
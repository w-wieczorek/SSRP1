from statistics import mean
from timeit import default_timer as timer
import argparse
import logging
from typing import List
from timeit import default_timer as timer

from ilp import find_solution


def run_test(I: List[str], k: int) -> List[str]:    
    return find_solution(I, k)    
    

def run_tests(file_name: str, k: int):
    I: List[str] = [l.strip() for l in open(file_name, 'r').readlines()]
    
    start = timer()

    best_sol = run_test(I, k)

    logger = logging.Logger('ilp')
    logger.addHandler(logging.FileHandler('log_ilp', mode='a'))
    logger.info(f'{file_name}\t{len(I)}\t{len(I[0])}\t{k}\t{timer() - start}\t{len(best_sol)}')        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()    
    parser.add_argument("--file", action='store', type=str)
    parser.add_argument("--k", action='store', required=False, type=int)
    
    args = parser.parse_args()
    
    run_tests(args.file, args.k)    

import argparse
import logging
from statistics import mean
from typing import List
from glob import glob
from os.path import isfile, join
import re

def load_file(file_name: str) -> List[str]:
    return [l.strip() for l in open(file_name, 'r').readlines()]


def run_tests(file_name: str, k: int, time_limit_sec: int, repeats: int):
    from ma import run_ga

    I: List[str] = load_file(file_name)

    solutions_lengths: List[int] = []

    for _ in range(repeats):
        init_solution = run_qcp(file_name, I, k, time_limit_sec//2)
        best_sol = run_ga(I, k, time_limit_sec//2, init_solution)
        solutions_lengths.append(best_sol)

    logger = logging.Logger('Hybrid')
    logger.addHandler(logging.FileHandler('log_hybrid', mode='a'))
    logger.info(f'{file_name}\t{len(I)}\t{len(I[0])}\t{k}\t{time_limit_sec}\t{mean(solutions_lengths)}\t{max(solutions_lengths)}') 
    

def run_qcp(file_name: str, I: List[str], k: int, time_limit_sec: int):    
    import qcpmodel as qcp
        
    n, m, alphabet_size = get_file_name_params(file_name)
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:int(alphabet_size)]

    data = qcp.InputData(int(n), int(m), int(k), alphabet, I)
    result: qcp.Result = qcp.BuildAndSolve(time_limit_sec, data)
    return result.x_vals

def get_file_name_params(file_name):
    file_name_regex = r"words_(?P<n>\d{3,4})_(?P<m>\d{4})_(?P<alphabet>\d{2})_0.\d+.dat"
    file_name_params_matches = re.search(file_name_regex, file_name)
    return file_name_params_matches.groups()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()    
    parser.add_argument("--file", action='store', type=str)
    parser.add_argument("--k", action='store', required=False, type=int)
    parser.add_argument("--time_limit_sec", action='store', required=False, type=int)
    parser.add_argument("--repeats", action='store', required=False, default=3, type=int)
    
    args = parser.parse_args()

    if isfile(args.file):
        run_tests(args.file, args.k, args.time_limit_sec, args.repeats)        
    else:        
        for file_name in glob(join(args.file, '*.dat')):            
            n, m, _ = get_file_name_params(file_name)
            print(f"File name: {file_name}")            
            run_tests(file_name, int(m) // 20, int(n), args.repeats)
            run_tests(file_name, int(m) // 10, int(n), args.repeats)
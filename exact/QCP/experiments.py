import argparse
import logging
from statistics import mean
from typing import List
from glob import glob
from os.path import isfile, join
import re
from timeit import default_timer as timer


def load_file(file_name: str) -> List[str]:
    return [l.strip() for l in open(file_name, 'r').readlines()]


def run_tests(file_name: str, k: int):    
    I: List[str] = load_file(file_name)

    start = timer()

    solution = run_qcp(file_name, I, k)            

    logger = logging.Logger('QCP')
    logger.addHandler(logging.FileHandler('log_qcp', mode='a'))
    logger.info(f'{file_name}\t{len(I)}\t{len(I[0])}\t{k}\t{timer() - start}\t{solution}') 
    

def run_qcp(file_name: str, I: List[str], k: int):    
    import qcpmodel as qcp
        
    n, m, alphabet_size = get_file_name_params(file_name)
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:int(alphabet_size)]

    data = qcp.InputData(int(n), int(m), int(k), alphabet, I)
    result: qcp.Result = qcp.BuildAndSolve(data)
    return sum(result.x_vals)

def get_file_name_params(file_name):
    file_name_regex = r"words_(?P<n>\d{3,4})_(?P<m>\d{4})_(?P<alphabet>\d{2})_0.\d+.dat"
    file_name_params_matches = re.search(file_name_regex, file_name)
    return file_name_params_matches.groups()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()    
    parser.add_argument("--file", action='store', type=str)
    parser.add_argument("--k", action='store', required=False, type=int)
    
    args = parser.parse_args()
    
    run_tests(args.file, args.k)        

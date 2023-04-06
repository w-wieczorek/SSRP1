from ast import Assert
import sys
from typing import List, Dict
from collections import Counter


def greedy_f(I: List[str], k: int) -> List[str]: # O(2*m*n) + O(m)
    most_frequent_idx = select_first(I)
    S = make_solution_complete(I, k, most_frequent_idx)
    return S


def bc_all(Sp: List[Dict[str, int]], s: str) -> int: # O(m)
    m = len(s)
    return sum(1 for j in range(m) if len(Sp[j]) > 1 or s[j] not in Sp[j])


def bc_each(Sp: List[str], s: str) -> int: # O(n*m)
    m = len(s)        
    bc, result = 0, 0
    for p in Sp:
        result = sum(1 for j in range(m) if p[j] != s[j])
        bc = max(bc, result)
    return bc


def make_solution_complete(I: List[str], k: int, Sp: int) -> List[str]:    
    m = len(I[0])
    S: List[str] = [I[Sp]]

    Sp_occurance = [{I[Sp][j]: 1} for j in range(m)] # O(m) 

    # checking k is not required
    Remining = [word for i, word in enumerate(I) if i != Sp] # O(n)
    
    while True:
        min_bc, min_idx = sys.maxsize, None    
        for i in range(len(Remining)):
            i_bc = bc_all(Sp_occurance, Remining[i])
            # i_bc = bc_each(S, Remining[i])
            if min_bc > i_bc and i_bc <= k:
                min_bc, min_idx = i_bc, i
        
        if min_idx is None:
            break

        for j in range(m):
            c = Remining[min_idx][j]
            Sp_occurance[j][c] = 1 + Sp_occurance[j].get(c, 0)
        
        S.append(Remining.pop(min_idx))            

    return S


def select_first(I: List[str]) -> int: # O(2*m*n)
    m = len(I[0])
    n = len(I)

    counters = [
        Counter(I[i][j] for i in range(n))
        for j in range(m)
    ] # O(m*n)

    max_sum, max_idx = -1, -1

    for i in range(n): # O(n*m)
        sum_i = sum(counters[j][I[i][j]] for j in range(m))
        if max_sum < sum_i:
            max_sum, max_idx = sum_i, i
    
    return max_idx


if __name__ == '__main__':    
    assert select_first(['abd', 'abc', 'abc', 'abg']) == 1
    
    assert select_first(['abb', 'dac', 'abc', 'abg']) == 2    

    bc_test_set = [{'a': 1}, {'a': 4, 'b': 5}, {'c': 1}]
    assert bc_all(bc_test_set, 'abc') == 1    
    assert bc_all(bc_test_set, 'gbc') == 2
    
    assert bc_each(['abc', 'abg', 'abm'], 'abd') == 1
    assert bc_each(['abc', 'abg', 'abm'], 'aff') == 2
    assert bc_each(['abg', 'amc', 'dbc'], 'abc') == 1

    assert make_solution_complete(['abg', 'abn', 'abm', 'abc', 'dab', 'afm', 'hrc'], 1, 3) == ['abc', 'abg', 'abn', 'abm']
    assert make_solution_complete(['abc', 'fff', 'ann', 'afc', 'agg', 'afm', 'hrc'], 2, 0) == ['abc', 'afc', 'ann', 'agg', 'afm']    

    assert greedy_f(['abg', 'abn', 'abm', 'abc', 'dac', 'afm', 'hrc'], 1) == ['abc', 'abg', 'abn', 'abm']


from typing import List, Set, Tuple, Dict

import numpy as np


def diff(s1: str, s2: str, k: int) -> Set[int]:
    counter = 0
    result: List[str] = []
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            if counter == k:
                return None
            
            counter += 1
            result.append(i)

    return set(result)


def diff_vector(excluded_words: List[int], I: List[List[str]], k: int) -> int:
    curr_k = 0
    for i in range(len(I[0])):
        char = None
        for j in range(len(I)):
            if excluded_words[j] == 0:
                continue
            elif not char:
                char = I[j][i]
            elif char != I[j][i]:
                if k > curr_k:
                    curr_k+=1
                    break
                else:
                    return curr_k + 1
    return curr_k


def diff_np(s1: str, s2: str) -> List[int]:
    return np.array([1 if s1[i] != s2[i] else 0 for i in range(len(s1))], dtype=int)

def get_diff_vector(I: List[str]):
    diff: Dict[Tuple[int, int], List[int]] = {}

    for i in range(len(I)):        
        for j in range(i+1, len(I)):
            diff[(i,j)] = diff_np(I[i], I[j])
    
    return diff

def diff_vector2(diff_vectors: Dict[Tuple[int, int], List[int]], solution: List[int], m: int) -> int:
    sum_vec = np.zeros(m)
    for i in np.flatnonzero(solution):
        for j in np.flatnonzero(solution):
            if i < j:
              sum_vec += diff_vectors[(i,j)]

    return np.count_nonzero(sum_vec)

def build_graph(I: List[str], k: int) -> List[List[Set[int]]]:
    mat: List[List[Set[int]]] = []
    for i in range(len(I)):
        conn = [None] * (i+1)
        for j in range(i+1):
            conn[j] = diff(I[i], I[j], k) if i != j else None

        mat.append(conn)

    return mat


def has_edge(n1: int, n2: int, mat: List[List[Set[int]]]) -> Tuple[bool, Set[int]]:
    n1,n2 = (n1,n2) if n1 > n2 else (n2, n1)
    value = mat[n1][n2]
    if value:
        return True, value
    
    return False, None


def run_ut():            
    assert diff("aab", "aab", 3) == set()
    assert diff("aaa", "aab", 3) == {2}
    assert diff("aaa", "bab", 3) == {0,2}
    assert diff("aaa", "bbb", 4) == {0,1,2}
    assert diff("aaa", "bbb", 1) is None

    assert build_graph(["ABBC", "ABCC", "BBCC", "CCCC"], 2) == [[None], [{2}, None], [{0,2},{0}, None], [None, {0,1}, {0,1}, None]]

    gr = build_graph(["ABBC", "ABCC", "BBCC", "CCCC"], 2)
    assert has_edge(0, 3, gr) == (False, None)
    assert has_edge(0, 1, gr) == (True, {2})
    assert has_edge(0, 2, gr) == (True, {0,2})
    assert has_edge(1, 2, gr) == (True, {0})
    assert has_edge(0, 2, gr) == has_edge(2, 0, gr)
    assert has_edge(0, 3, gr) == has_edge(3, 0, gr)

    assert diff_vector([0,0,1], ["abc","def","ghi"], 5) == 0
    assert diff_vector([0,1,0], ["abc","def","ghi"], 5) == 0
    assert diff_vector([1,0,0], ["abc","def","ghi"], 5) == 0

    assert diff_vector([0,0,1], ["abc","def","ghi"], 0) == 0
    assert diff_vector([0,1,0], ["abc","def","ghi"], 0) == 0
    assert diff_vector([1,0,0], ["abc","def","ghi"], 0) == 0

    assert diff_vector([0,1,1], ["abc","add","agg"], 2) == 2
    assert diff_vector([0,1,1], ["abc","def","ghi"], 2) == 3
    assert diff_vector([0,1,1], ["abc","def","ghi"], 1) == 2
    assert diff_vector([1,0,1], ["abc","def","bbi"], 2) == 2
    assert diff_vector([1,0,1], ["abc","def","abi"], 2) == 1
    assert diff_vector([0,0,0], ["abc","def","abi"], 2) == 0
    assert diff_vector([1,1,1], ["abc","dbe","fbg"], 2) == 2
    assert diff_vector([1,1,1], ["acb","deb","fgb"], 2) == 2
    assert diff_vector([1,1,1], ["acb","deb","fgb"], 3) == 2
    assert diff_vector([1,1,1], ["acb","deb","fgb"], 1) == 2

    diff_v = get_diff_vector(["acb","feb","fgb"])
    assert np.array_equal(diff_v[(0,1)], np.array([1,1,0], dtype=int))
    assert np.array_equal(diff_v[(0,2)], np.array([1,1,0], dtype=int))
    assert np.array_equal(diff_v[(1,2)], np.array([0,1,0], dtype=int))
    assert not np.array_equal(diff_v[(1,2)], np.array([1,1,1], dtype=int))

    diff_v = get_diff_vector(["abcd","defg","ghij"])
    assert diff_vector2(diff_v, np.array([1,1,1]), 4) == 4

    diff_v = get_diff_vector(["abcd","abgg","ghij"])
    assert diff_vector2(diff_v, np.array([1,1,0]), 4) == 2

    diff_v = get_diff_vector(["abcd","aggd","ammd"])
    assert diff_vector2(diff_v, np.array([1,1,1]), 4) == 2

    diff_v = get_diff_vector(["abcd","dggd","dmmd"])
    assert diff_vector2(diff_v, np.array([1,1,1]), 4) == 3

    print('Done')


if __name__ == '__main__':
    run_ut()
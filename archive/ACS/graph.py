from typing import List, Set, Tuple


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

    print('Done')


if __name__ == '__main__':
    run_ut()
from typing import List
from random import sample

def destroy_partially(Sp: List[str], perc_dest: int) \
     -> List[str]:
    d = len(Sp) * perc_dest // 100
    return sample(Sp, k=len(Sp) - d)


if __name__ == '__main__':
    test_result = destroy_partially(['abc','def','ghi','jkl','mno','prs','tuw', 'xyz', 'abc2', 'def2'], 30)    
    assert len(test_result) == 7
    assert len(test_result) == len(set(test_result))
    print(test_result)


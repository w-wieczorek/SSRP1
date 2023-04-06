from typing import Sequence, List
from random import choices, random, choice
from copy import copy
from os.path import join


def generate(n: int, m: int, alphabet: Sequence, pc: float) -> List[str]:
    root_word = ''.join(choices(alphabet, k=m))
    words = [root_word]
    for _ in range(n - 1):

        while True:
            changed = False
            new_word = list(copy(root_word))  # always start from scratch
            for i in range(m):
                if random() < pc:
                    new_word[i] = choice(alphabet)
                    changed = new_word[i] != root_word[i]

            word = ''.join(new_word)
            if changed:
                words.append(word)
                break

    return words


def generate_and_save(path: str, n: int, m: int, alphabet: Sequence, pc: float):
    words = generate(n, m, alphabet, pc)
    with open(join(path, f'words_{n:03}_{m:04}_{len(alphabet):02}_{pc:.3f}.dat'), "w") as f:
        f.write('\n'.join(words))


alph = [chr(i) for i in range(ord('A'), ord('Z'))]
path = '.'

for n in [200]:
    for m in [500]:
        for alphabet_size in [4, 12, 20]:
            pcs_dict = {
                100: [0.01, 0.03, 0.05],
                200: [0.01, 0.03, 0.05],
                500: [0.005, 0.015, 0.025],
                1000: [0.01, 0.03, 0.005],
                2000: [0.001, 0.003, 0.005],
                4000: [0.001, 0.003, 0.005],
                5000: [0.01, 0.03, 0.005],
            }            
            for pc in pcs_dict[n]:
                generate_and_save(path, n, m, alph[:alphabet_size], pc)

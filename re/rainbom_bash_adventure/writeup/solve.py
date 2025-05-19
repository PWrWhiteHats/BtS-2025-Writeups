import random
import hashlib
from collections import defaultdict

import numpy as np


flag = b""


def xor(target, key):
    out = [c ^ key[i % len(key)] for i, c in enumerate(target)]
    return bytearray(out)


def key_from_path(path):
    return hashlib.sha256(str(path).encode()).digest()


def check_path(path, enc_flag):
    global flag
    flag1 = xor(enc_flag, key_from_path(path))
    flag2 = xor(enc_flag, key_from_path(list(reversed(path))))
    print(path)
    if flag1.startswith(b"BtSCTF"):
        flag = flag1
        print(flag)
        flag = bytes(flag).replace(b"{", b"{{").decode('ascii')
        return True
    if flag2.startswith(b"BtSCTF"):
        flag = flag2
        print(flag)
        flag = bytes(flag).replace(b"{", b"{{").decode('ascii')
        return True
    return False


class Graph:
    def __init__(self, size):
        self.size = size
        self.nodes = defaultdict(lambda : {})

    def get_matrix(self):
        m = [[0 for _ in range(self.size)] for _ in range(self.size)]
        for v, neighbours in self.nodes.items():
            for neighbour, weight in neighbours.items():
                m[v][neighbour] = weight
        return m

if __name__ == '__main__':
    random.seed(0xc0fe)
    g = Graph(20)
    f = open("rainbow bash adventure/game/script.rpy", "r")
    c = f.read()
    labels = c.split('label cloud')[1:]
    labels[-1] = labels[-1].split('label ending:')[0]


    for label in labels:
        node = int(label.split(':')[0])
        for line in label.split('\n'):
            if 'which is' not in line:
                continue
            to = int(line.split('to cloud')[1].split(' which')[0])
            weight = int(line.split('which is ')[1].split(' pony')[0])
            if node == to:
                continue
            print(node, to)
            g.nodes[node][to] = weight
            g.nodes[to][node] = weight

    import solvers
    solver = solvers.GeneticTSP(
        distance_matrix=np.array(g.get_matrix()),
        population_size=200,
        mutation_rate=0.1,
        elitism_rate=0.1
    )
    perm, dist = solver.solve(8)
    print(dist)
    print(perm)
    while perm[0] != 0:
        perm.append(perm.pop(0))
    perm.append(0)
    is_correct = check_path(perm, bytearray(b'\xc2\x92\xf9\xf66\xe8\xa5\xa6\x17\xb6mGE\xcfQ\x90Mk:\x9a\xbb\x905&\x19\x8e\xc4\x9a\x0b\x1f\xf8C\xf4\xb9\xc9\x85R\xc2\xbb\x8d\x07\x94[R_\xf5z\x9fAl\x11\x9c\xbb\x9255\x08\x8e\xf6\xd6\x04'))




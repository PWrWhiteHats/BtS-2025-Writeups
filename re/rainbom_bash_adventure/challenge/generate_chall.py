import random
import hashlib
from collections import defaultdict

import numpy as np
# from python_tsp.heuristics import solve_tsp_simulated_annealing


BEGINNING = '''
define twi = Character("Twilyght Spakyl")
define rb = Character("Rainbom Bash")
define fs = Character("Flubbershy")

label start:
    $ nodes = [0]
    scene bg1
    with dissolve
    with fade
    with pixellate
    with wipeleft
    with wiperight
    show rb at left
    with hpunch
    with vpunch
    with moveinbottom
    with moveinright
    
    "Rainbom Bash wake up in mornin, cloudz all over"
    
    rb "ughh not cloudz again. i hate cloudz"
    
    show fs at right
    with zoomin
    with moveinleft
    with hpunch
    
    rb "flubbershy qwick come i gotta smash cloudz"
    fs "cant i got zen day"
    rb "and i dont like cloud"
    
    with vpunch
    with hpunch
    
    fs "zen day very important for my animal friends"
    
    rb "more important than smashin cloudz?"
    
    fs "yes zen make me calm for whole week"
    
    rb "fine i find somepony else to help"
    
    with dissolve
    with pixellate
    with blinds
    
    fs "mayb ask spakyl she always know what do"
    
    rb "spakyl always make me do all work anyway"
    
    hide fs
    with moveoutright
    with vpunch
    with dissolve
    
    hide rb
    with moveoutleft
    with hpunch
    with pixellate
    
    scene bg2
    with squares
    with blinds
    with dissolve
    with fade
    
    "Later at spakyl house with all the book"
    
    show rb at left
    with moveinleft
    with vpunch
    
    show twi at right
    with moveinright
    with zoomin
    with hpunch
    
    twi "rainbom bash qwick come cloudz is everywher"
    rb "cant im already layin"
    twi "rainbom now is not time for layin"
    rb "then do it yurself if u so smart"
    twi "i got no wing only brain"
    rb "then let ur brain do flyin"
    
    with pixellate
    with dissolve
    with squares
    
    twi "my brain too heavy for flyin"
    
    rb "then what we do about cloudz"
    
    twi "u must smash them all before sunset"
    
    rb "too many cloudz for one pony"
    
    twi "u strongest flyer in ponyville u can do it"
    
    rb "but i was plannin on layin all day"
    
    with vpunch
    with hpunch
    
    twi "layin can wait cloudz cannot"
    
    rb "ughhh fine but u owe me big nap after"
    
    hide rb
    with moveoutbottom
    with vpunch
    with pixellate
    
    twi "she best cloud smasher when not busy layin"
    
    "Help Rainbom Bash smash all the clouds in the fastest possible way and return to the origin.
    I heard it's a well known problem..."
    jump cloud0

'''

ENDING = '''
label ending:
    python:
        import hashlib


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
            if flag1.startswith(b"BtSCTF"):
                flag = flag1
                print(flag)
                flag = bytes(flag).replace(b"{{", b"{{{{").decode('ascii')
                return True
            if flag2.startswith(b"BtSCTF"):
                flag = flag2
                print(flag)
                flag = bytes(flag).replace(b"{{", b"{{{{").decode('ascii')
                return True
            return False


        is_correct = check_path(nodes, {})
    if is_correct:
        rb "all cloudz smashed im the queen"
        rb "i got 100% swag"
        "[flag]"
    else:
        "Sadly, Rainbom Bash was too slow and wasn't able to smash all clouds."
    return

'''


def xor(target, key):
    out = [c ^ key[i % len(key)] for i, c in enumerate(target)]
    return bytearray(out)


def key_from_path(path):
    return hashlib.sha256(str(path).encode()).digest()


def check_path(path, enc_flag):
    if xor(enc_flag, key_from_path(path)).startswith(b"BtSCTF"):
        return True
    if xor(enc_flag, key_from_path(list(reversed(path)))).startswith(b"BtSCTF"):
        return True
    return False


class Graph:
    def __init__(self, size):
        self.size = size
        self.nodes = defaultdict(lambda : {})
        self.optimal_path = list(range(1, self.size))
        random.shuffle(self.optimal_path)
        self.optimal_path = [0] + self.optimal_path + [0]
        self.optimal_solution = 0
        self.generate_graph()

    def get_enc_flag(self):
        flag = b"BtSCTF{YOU_are_getting_20_percent_c00ler_with_this_one_!!_B)}"
        return xor(flag, key_from_path(self.optimal_path))

    def generate_graph(self):
        for n, m in zip(self.optimal_path,
                        self.optimal_path[1:]+self.optimal_path[:1]):
            self.nodes[n][m] = random.randrange(0x1_000_000, 0x1_200_000)
            self.nodes[m][n] = self.nodes[n][m]
            self.nodes[n][n] = 0
            self.optimal_solution += self.nodes[m][n]
            for i in range(self.size):
                if i in self.nodes[n].keys():
                    continue
                self.nodes[n][i] = random.randrange(0x1_800_000, 0x2_000_000)
                self.nodes[i][n] = self.nodes[n][i]

    def get_matrix(self):
        m = [[0 for _ in range(self.size)] for _ in range(self.size)]
        for v, neighbours in self.nodes.items():
            for neighbour, weight in neighbours.items():
                m[v][neighbour] = weight
        return m

    def generate_dispatch(self):
        dispatch = ""
        dispatch += "label dispatch:\n"
        dispatch += f"    if len(nodes) == {len(self.nodes)+1}:\n"
        dispatch += f"        jump ending\n"
        for n in self.nodes.keys():
            dispatch += f"    if nodes[-1] == {n}:\n"
            dispatch += f"        jump cloud{n}\n"
        return dispatch

    def generate_vn_nodes(self):
        ret = ""
        for node, neighbours in self.nodes.items():
            ret += f"label cloud{node}:\n"
            ret += "menu:\n"
            for neighbour, weight in neighbours.items():
                ret += f'    "fly to cloud{neighbour} which is {weight} pony units away":\n'
                ret += f"        $ nodes.append({neighbour})\n"
                ret += "        jump dispatch\n"
        return ret


if __name__ == '__main__':
    random.seed(0xc0fe)
    g = Graph(20)
    enc_flag = g.get_enc_flag()
    assert check_path(g.optimal_path, enc_flag)
    assert not check_path([9999] + g.optimal_path, enc_flag)

    print(f"{g.optimal_solution=}")

    import solvers
    solver = solvers.GeneticTSP(
        distance_matrix=np.array(g.get_matrix()),
        population_size=200,
        mutation_rate=0.5,
        elitism_rate=0.5
    )
    perm, dist = solver.solve(4)
    print(dist)
    print(perm)
    print(g.optimal_path)
    assert int(dist) == g.optimal_solution

    outfile = open("rainbow bash adventure/game/script.rpy", "w")
    print(BEGINNING, file=outfile)
    print(g.generate_dispatch(), file=outfile)
    print(g.generate_vn_nodes(), file=outfile)
    print(ENDING.format(str(enc_flag)), file=outfile)

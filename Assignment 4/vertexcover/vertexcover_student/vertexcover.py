#! /usr/bin/env python3
"""NAMES OF THE AUTHOR(S): Nicolas Golenvaux <nicolas.golenvaux@uclouvain.be>"""
from matplotlib.pyplot import step
from search import *
import sys
import time
import os

used_covers = set()

class VertexCover(Problem):

    def __init__(self, initial, goal=None):
        super().__init__(initial, goal)

    # if you want you can implement this method and use it in the maxvalue and randomized_maxvalue functions
    # neighborhood relation
    def successor(self, state):
        global used_covers
        successors = []
        worse_successors = []
        for old_vertice_index in range(len(state.cover)):
            for new_vertice in state.not_cover:
                new_cover = state.cover.copy()
                new_cover[old_vertice_index] = new_vertice
                if tuple(new_cover) in used_covers:
                    worse_successors.append((None, State(k=state.k, vertices=state.vertices, edges=state.edges, cover=new_cover)))
                    # continue
                used_covers.add(tuple(new_cover))
                # appending None as action along with the new state, because it is not used but is necessary for the successor function
                successors.append((None, State(k=state.k, vertices=state.vertices, edges=state.edges, cover=new_cover)))
        return successors if len(successors) > 0 else worse_successors
        # return successors

    # if you want you can implement this method and use it in the maxvalue and randomized_maxvalue functions
    def value(self, state):
        return state.score


class State:

    def __init__(self, k, vertices, edges, cover=None, not_cover=None):
        self.k = k
        self.n_vertices = len(vertices)
        self.vertices = vertices
        self.n_edges = len(edges)
        self.edges = edges
        if cover is None:
            self.cover = self.build_init()
        else:
            self.cover = cover
        if not_cover is None:
            self.not_cover = [v for v in range(self.n_vertices) if v not in self.cover]
        else:
            self.not_cover = not_cover
        # the score is the number of edges that are covered
        self.score = self.compute_score()

    # an init state building is provided here but you can change it at will
    def build_init(self):
        return list(range(self.k))

    def compute_score(self):
        score = 0
        for v1, v2 in self.edges.values():
            if v1 in self.cover or v2 in self.cover:
                score += 1
        return score

    def __str__(self):
        s = '\\{'
        for v in self.cover:
            s += str(v) + ','
        return s[:-1]+'\\}'

# k is the size of the best subset to find
# vertices[i] is the list of edges that are connected to vertice i
# edges[i] is the pair of vertices that are connected by edge i
def read_instance(instanceFile):
    file = open(instanceFile)
    line = file.readline()
    k = int(line.split(' ')[0])
    n_vertices = int(line.split(' ')[1])
    n_edges = int(line.split(' ')[2])
    vertices = {}
    for i in range(n_vertices):
        vertices[i] = []
    edges = {}
    line = file.readline()
    while line:
        [edge,vertex1,vertex2] = [int(x) for x in line.split(' ')]
        vertices[vertex1] += [edge]
        vertices[vertex2] += [edge]
        edges[edge] = (vertex1,vertex2)
        line = file.readline()
    return k, vertices, edges


# Attention : Depending of the objective function you use, your goal can be to maximize or to minimize it
def maxvalue(problem, limit=100, callback=None):
    current = LSNode(problem, problem.initial, 0)
    best = current

    for step in range(limit):
        if callback is not None:
            callback(current)
        successors = problem.successor(current.state)
        if len(successors) == 0:
            return best
        # sort successors based on their score
        successors.sort(key=lambda x: x[1].score, reverse=True)
        # new node is initialized with the best successor
        current = LSNode(problem, successors[0][1], current.step + 1)
        if current.value() > best.value():
            best = current

    return best

# Attention : Depending of the objective function you use, your goal can be to maximize or to minimize it
def randomized_maxvalue(problem, limit=100, callback=None):
    current = LSNode(problem, problem.initial, 0)
    best = current

    for step in range(limit):
        if callback is not None:
            callback(current)
        successors = problem.successor(current.state)
        best_of_n = 5
        if len(successors) < 5:
            best_of_n = len(successors)
        # sort successors based on their score
        successors.sort(key=lambda x: x[1].score, reverse=True)
        # select a random successor from the 5 best ones
        current = LSNode(problem, successors[random.randint(0, best_of_n-1)][1], current.step + 1)
        if current.value() > best.value():
            best = current

    return best


#####################
#       Launch      #
#####################
if __name__ == '__main__':
    for file in os.listdir("instances"):
        info = read_instance("instances/" + file)
        init_state = State(k=info[0], vertices=info[1], edges=info[2])
        vc_problem = VertexCover(init_state)
        step_limit = 100
        start = time.perf_counter()
        for _ in range(10):
            node = random_walk(vc_problem, step_limit)
            used_covers.clear()
        end = time.perf_counter()
        nstep = node.step
        score = node.state.score
        with open("result.txt", "a") as f:
            f.write(f"{random_walk.__name__} with {file}:\tT={(end-start)/10:.2e}\tS={nstep}\tV={score}\n")
        used_covers.clear()
    # info = read_instance(sys.argv[1])
    # init_state = State(info[0], info[1], info[2])
    # vc_problem = VertexCover(init_state)
    # step_limit = 100
    # node = maxvalue(vc_problem, step_limit)
    # state = node.state
    # print(state)

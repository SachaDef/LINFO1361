#! /usr/bin/env python3
"""NAMES OF THE AUTHOR(S): Nicolas Golenvaux <nicolas.golenvaux@uclouvain.be>"""
from search import *
import sys


class VertexCover(Problem):

    # if you want you can implement this method and use it in the maxvalue and randomized_maxvalue functions
    def successor(self, state):
        pass

    # if you want you can implement this method and use it in the maxvalue and randomized_maxvalue functions
    def value(self, state):
        pass


class State:

    def __init__(self, k, vertices, edges, cover=None, not_cover=None):
        self.k = k
        self.n_vertices = len(vertices)
        self.n_edges = len(edges)
        self.vertices = vertices
        self.edges = edges
        if cover is None:
            self.cover = self.build_init()
        else:
            self.cover = cover
        if not_cover is None:
            self.not_cover = [v for v in range(self.n_vertices) if v not in self.cover]
        else:
            self.not_cover = not_cover

    # an init state building is provided here but you can change it at will
    def build_init(self):
        return list(range(self.k))

    def __str__(self):
        s = ''
        for v in self.cover:
            s += ' ' + str(v)
        return s


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

    # Put your code here

    return best

# Attention : Depending of the objective function you use, your goal can be to maximize or to minimize it
def randomized_maxvalue(problem, limit=100, callback=None):
    current = LSNode(problem, problem.initial, 0)
    best = current

    # Put your code here

    return best


#####################
#       Launch      #
#####################
if __name__ == '__main__':
    info = read_instance(sys.argv[1])
    init_state = State(info[0], info[1], info[2])
    vc_problem = VertexCover(init_state)
    step_limit = 100
    node = randomized_maxvalue(vc_problem, step_limit)
    state = node.state
    print(state)

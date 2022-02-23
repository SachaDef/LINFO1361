"""
Name of the author(s):
- Louis Navarre <louis.navarre@uclouvain.be>
"""
import time
import sys
from search import *


###############
# State class #
###############
class State:

    def __init__(self, shape: tuple, grid: list, answer: list=None, move: str="Init") -> None:
        self.shape = shape
        self.answer = answer
        self.grid = grid
        self.move = move

    def __str__(self):
        s = self.move + "\n"
        for line in self.grid:
            s += "".join(line) + "\n"
        return s


#################
# Problem class #
#################
class Rubik2D(Problem):

    def actions(self, state: State) -> list:
        act = []
        m, n = state.shape
        for i in range(m):
            act.append(f"r{i}")
        for j in range(n):
            act.append(f"c{j}")
        return act

    def result(self, state: State, action: str) -> State:
        new_grid = state.grid
        if action[0] == "r":
            index = int(action[1])
            old_tup = new_grid[index]
            new_tup = old_tup[-1] + old_tup[1:]
            new_grid[index] = new_tup
        else:
            index = int(action[1])
            m, n = state.shape
            m = m-1
            for i in range(m):
                old_tup = new_grid[m-i]
                new_tup = old_tupe[:index] + (state.grid[m-i-1][index],) + old_tup[index+1:]
                new_grid[m-i] = new_tup
            old_tup = new_grid[0]
            new_tup = old_tupe[:index] + (state.grid[m][index],) + old_tup[index+1:]
            new_grid[0] = new_tup
        new_state = State(state.shape, new_grid, state.answer, action)
        
        return new_state

    def goal_test(self, state):
        pass



def read_instance_file(filepath):
    with open(filepath) as fd:
        lines = fd.read().splitlines()

    shape_x, shape_y = tuple([int(i) for i in lines[0].split(" ")])
    initial_grid = list()
    for row in lines[1:1 + shape_x]:
        initial_grid.append(tuple([i for i in row]))

    goal_grid = list()
    for row in lines[1 + shape_x + 1:]:
        goal_grid.append(tuple([i for i in row]))

    return (shape_x, shape_y), initial_grid, goal_grid


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: ./rubik2D.py <path_to_instance_file>")
    filepath = sys.argv[1]

    shape, initial_grid, goal_grid = read_instance_file(filepath)

    init_state = State(shape, tuple(initial_grid), tuple(goal_grid), "Init")
    problem = Rubik2D(init_state)

    # Example of search
    start_timer = time.perf_counter()
    node, nb_explored, remaining_nodes = breadth_first_tree_search(problem)
    end_timer = time.perf_counter()

    # Example of print
    path = node.path()

    for n in path:
        # assuming that the __str__ function of state outputs the correct format
        print(n.state)

    print("* Execution time:\t", str(end_timer - start_timer))
    print("* Path cost to goal:\t", node.depth, "moves")
    print("* #Nodes explored:\t", nb_explored)
    print("* Queue size at goal:\t",  remaining_nodes)

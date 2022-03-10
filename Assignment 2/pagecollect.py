from __future__ import annotations
from search import *
import time
import copy
###############
# State class #
###############
class State:
    def __init__(self, grid: list, cost: int=0, player_pos: tuple=(0, 0), n_pages: int=0, pages_pos: list=[], heuristic: int=0) -> None:
        self.nbr = len(grid)
        self.nbc = len(grid[0])
        self.grid = grid
        self.cost = cost
        self.player_pos = player_pos
        self.n_pages = n_pages
        self.pages_pos = pages_pos
        self.heuristic = heuristic

    def __str__(self) -> str:
        return '\n'.join(''.join(row) for row in self.grid)

    def __eq__(self, other_state: State) -> bool:
        return other_state.grid == self.grid

    def __hash__(self) -> int:
        tuple_grid = (tuple(l) for l in self.grid)
        return hash(tuple_grid)
    
    def __lt__(self, other: State) -> bool:
        self_f = self.cost + self.heuristic
        other_f = other.cost + other.heuristic
        return self_f < other_f
        
    def from_string(string: str) -> State:
        lines = string.strip().splitlines()
        return State(list(
            map(lambda x: list(x.strip()), lines)
        ))


def dist_man(pos1, pos2) -> int:
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def h(state: State, final_pos: tuple) -> int:
    h = 0
    if (state.n_pages !=0):
        for i in range(state.n_pages):
            h += dist_man(state.player_pos, state.pages_pos[i])
    else:
        h += dist_man(state.player_pos, final_pos)
    return h


#################
# Problem class #
#################
class PageCollect(Problem):

    def __init__(self, initial: State) -> None:
        final_goal = []
        n_pages = 0
        pages_pos = []
        for nth_row in range(initial.nbr):
            goal_row = []
            for nth_col in range(initial.nbc):
                if initial.grid[nth_row][nth_col] == "@":
                    goal_row.append(" ")
                    initial.player_pos = (nth_col, nth_row)
                elif initial.grid[nth_row][nth_col] == "p":
                    goal_row.append(" ")
                    n_pages += 1
                    pages_pos.append((nth_col, nth_row))
                elif initial.grid[nth_row][nth_col] == "X":
                    goal_row.append("@")
                    self.goal_pos = (nth_col, nth_row)
                else:
                    goal_row.append(initial.grid[nth_row][nth_col])
            final_goal.append(goal_row)
        initial.n_pages = n_pages
        initial.pages_pos = pages_pos
        goal = State(final_goal, 0, self.goal_pos, 0, [], 0)
        super().__init__(initial, goal=goal)
        # print(initial.grid[2])
        # print(initial)
        # print(goal)
        # print(self.n_pages)
        # print(self.pages_pos)
        # print(self.goal_pos)

        # self.n_ways = factorial(self.n_pages)
        # pages_order = []
        # for i in range(self.n_ways):
        

        

    def actions(self, state: State) -> list:
        acts = []
        grid = state.grid
        # print(state.player_pos)
        player_x, player_y = state.player_pos
        if grid[player_y+1][player_x] != "#":
            # print(grid[player_y+1][player_x])
            acts.append("s")
        if grid[player_y-1][player_x] != "#":
            # print(grid[player_y-1][player_x])
            acts.append("n")
        if grid[player_y][player_x+1] != "#":
            # print(grid[player_y][player_x+1])
            acts.append("e")
        if grid[player_y][player_x-1] != "#":
            # print(grid[player_y][player_x-1])
            acts.append("w")
        # print(acts)
        return acts

    
    def result(self, state: State, action: str) -> State:
        grid = copy.deepcopy(state.grid)
        old_x, old_y = state.player_pos

        if action == 's':
            new_x, new_y = old_x, old_y+1
        elif action == 'n':
            new_x, new_y = old_x, old_y-1
        elif action == 'e':
            new_x, new_y = old_x+1, old_y
        elif action == 'w':
            new_x, new_y = old_x-1, old_y
        
        n_pages = state.n_pages
        pages_pos = copy.deepcopy(state.pages_pos)
        if grid[new_y][new_x] == "p":
            n_pages -= 1
            pages_pos.remove((new_x, new_y))
        
        grid[old_y][old_x] = " "
        grid[new_y][new_x] = "@"

        new_state = State(grid, state.cost+1, (new_x, new_y), n_pages, pages_pos, 0)
        # print("fct result")
        # print(new_state)
        new_state.heuristic = h(new_state, self.goal_pos)
        return new_state

    def goal_test(self, state: State) -> bool:
        return state == self.goal
    
    def h(self, node: Node) -> int:
        h = 0
        if (node.state.n_pages !=0):
            for i in range(node.state.n_pages):
                h += dist_man(node.state.player_pos,node.state.pages_pos[i])
        else:
            h += dist_man(node.state.player_pos,self.goal_pos)
        # print("valeur de h = " + str(h))
        return h

    def load(path):
        with open(path, 'r') as f:
            lines = f.readlines()
            
        state = State.from_string(''.join(lines))
        return PageCollect(state)



#####################
# Launch the search #
#####################
problem = PageCollect.load(sys.argv[1])

# Example of search
start_timer = time.perf_counter()
node, nb_explored, remaining_nodes = breadth_first_graph_search(problem)
end_timer = time.perf_counter()

# example of print
path = node.path()

# print('Number of moves: ' + str(node.depth))
for n in path:
    print(n.state)  # assuming that the __str__ function of state outputs the correct format
    print()
print("* Execution time:\t", str(end_timer - start_timer))
print("* #Nodes explored:\t", nb_explored)
print('Number of moves: ' + str(node.depth))
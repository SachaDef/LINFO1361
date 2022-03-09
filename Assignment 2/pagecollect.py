from __future__ import annotations
from search import *
from scipy.special import factorial

###############
# State class #
###############
class State:
    def __init__(self, grid: list, cost: int=0, heuristic: float=0.0, player_pos: tuple=(0, 0)) -> None:
        self.nbr = len(grid)
        self.nbc = len(grid[0])
        self.grid = grid
        self.cost = cost
        self.heuristic = heuristic
        self.player_pos = player_pos

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


#################
# Problem class #
#################
class PageCollect(Problem):

    def __init__(self, initial: State) -> None:
        final_goal = []
        self.n_pages = 0
        self.pages_pos = []
        for nth_row in range(initial.nbr):
            goal_row = []
            for nth_col in range(initial.nbc):
                if initial.grid[nth_row][nth_col] == "@":
                    goal_row.append(" ")
                    initial.player_pos = (nth_col, nth_row)
                elif initial.grid[nth_row][nth_col] == "p":
                    goal_row.append(" ")
                    self.n_pages += 1
                    self.pages_pos.append((nth_col, nth_row))
                elif initial.grid[nth_row][nth_col] == "X":
                    goal_row.append("@")
                    self.goal_pos = (nth_col, nth_row)
                else:
                    goal_row.append(initial.grid[nth_row][nth_col])
            final_goal.append(goal_row)
        goal = State(final_goal, 0, 0, self.goal_pos)
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
        grid = state.grid
        old_x, old_y = state.player_pos

        if action == 's':
            new_x, new_y = old_x, old_y+1
        elif action == 'n':
            new_x, new_y = old_x, old_y-1
        if action == 'e':
            new_x, new_y = old_x+1, old_y
        elif action == 'w':
            new_x, new_y = old_x-1, old_y
        
        if grid[new_y][new_x] == "p":
            self.n_pages -= 1
            del self.pages_pos[self.pages_pos.index((new_x, new_y))]
        
        grid[old_y][old_x] = " "
        grid[new_y][new_x] = "@"

        return State(grid, state.cost+1, self.h(), (new_x, new_y))

    def goal_test(self, state: State) -> bool:
        return state == self.goal
    
    def h(self, node: Node) -> float:
        h = 0.0
        for i in range(self.n_pages):
            h += dist_man(node.state.player_pos,self.pages_pos[i])
        h += dist_man(node.state.player_pos,self.goal_pos)
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

node = astar_search(problem)

# example of print
path = node.path()

print('Number of moves: ' + str(node.depth))
for n in path:
    print(n.state)  # assuming that the __str__ function of state outputs the correct format
    print()

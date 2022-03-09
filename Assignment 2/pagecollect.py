from mimetypes import init
from typing_extensions import Self
from search import *
from __future__ import annotations


###############
# State class #
###############
class State:
    def __init__(self, grid: list) -> None:
        self.nbr = len(grid)
        self.nbc = len(grid[0])

    def __str__(self) -> str:
        '\n'.join(''.join(row) for row in self.grid)

    def __eq__(self, other_state: State) -> bool:
        return other_state.grid == self.grid

    def __hash__(self) -> int:
        tuple_grid = (tuple(l) for l in self.grid)
        pass
    
    def __lt__(self, other) -> bool:
        return hash(self) < hash(other)
    
    def from_string(string: str) -> State:
        lines = string.strip().splitlines()
        return State(list(
            map(lambda x: list(x.strip()), lines)
        ))


#################
# Problem class #
#################
class PageCollect(Problem):

    def __init__(self, initial: State) -> None:
        final_goal = []
        for row in initial.grid:
            goal_row = []
            for elem in row:
                if elem == "@" or elem == "p":
                    goal_row.append(" ")
                elif elem == "X":
                    goal_row.append("@")
                else:
                    goal_row.append(elem)
            final_goal.append(goal_row)
        super.__init__(initial, goal=final_goal)

    def actions(self, state: State) -> list:
        grid = state.grid

    
    def result(self, state: State, action: str) -> State:
        pass

    def goal_test(self, state: State) -> bool:
        pass
    
    def h(self, node: Node) -> float:
        h = 0.0
        # ...
        # compute an heuristic value
        # ...
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

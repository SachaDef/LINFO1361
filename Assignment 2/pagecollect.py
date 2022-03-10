from __future__ import annotations
from search import *
import time
import copy


####################
# Helper functions #
####################
def dist_man(pos1: tuple, pos2: tuple) -> int:
    """
    The dist_man function returns the manhattan distance between two points with 2D coordinates
    
    Arguments
    ---------
    pos1/pos2: tuples containing the (x, y) coordinates of the two points

    Returns
    -------
    The manhattan distance between the two points
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def h(state: State, final_pos: tuple) -> int:
    """
    The h function returns the heuristic value corresponding to a state given the final goal

    Arguments
    ---------
    state: a State instance to compute the heuristic value of
    final_pos: a tuple of int (x, y) of the goal's coordinates

    Returns
    -------
    A heuristic value computed by using the sum of the manhattan distances to each page, or to the goal if there
    are no more pages to collect
    """
    h = 0
    if (state.n_pages !=0):
        for i in range(state.n_pages):
            h += dist_man(state.player_pos, state.pages_pos[i])
    else:
        h += dist_man(state.player_pos, final_pos)
    return h


###############
# State class #
###############
class State:
    """
    The State class is used in AI problem solving to represent a precise reached step with various information about it.
    In this case, the State class is used in a pathfinding problem where you have to collect objects (pages) in the maze first
    (problem described in the PageCollect class below).
    
    Attributes
    ----------
    nbr/nbc (int): number of rows/columns in the maze (same for all states of the same problem)
    grid (matrix of str): representation of the maze, including the student, the pages to collect and the examiner
    cost/heuristic (int): values corresponding to the distance already travelled/an estimation of the distance left to travel
    player_pos (tuple of int): (x, y) position of the student in the maze
    n_pages/pages_pos (int/list of tuples of int): number of remaining pages to collect/their (x, y) position in the maze
    """

    def __init__(self, grid: list=[[]], cost: int=0, heuristic: int=0, player_pos: tuple=(0, 0), n_pages: int=0, pages_pos: list=[]) -> None:
        self.nbr = len(grid)
        self.nbc = len(grid[0])
        self.grid = grid
        self.cost = cost
        self.heuristic = heuristic
        self.player_pos = player_pos
        self.n_pages = n_pages
        self.pages_pos = pages_pos

    def __str__(self) -> str:
        return '\n'.join(''.join(row) for row in self.grid)

    def __eq__(self, other: State) -> bool:
        """
        The __eq__ method is used to compare two state instances, by comparing their respective grids

        Arguments
        ---------
        other_state: state instance to compare to

        Returns
        -------
        A boolean indicating whether or not the two state instances have the same grid
        """
        return other.grid == self.grid

    def __hash__(self) -> int:
        """
        The __hash__ method is used to obtain a hash value of the state instance by hashing its grid

        Returns
        -------
        An int value corresponding to the hash of the state's grid
        """
        tuple_grid = (tuple(l) for l in self.grid)
        return hash(tuple_grid)
    
    def __lt__(self, other: State) -> bool:
        """
        The __lt__ method is used to compare two state instances, by comparing the sum of their respective costs and heuristics

        Arguments
        ---------
        other: state instance to compare to

        Returns
        -------
        A boolen indicating whether or not the sum of the cost and heuristic of this instance is less than the one of the other
        instance
        """
        self_f = self.cost + self.heuristic
        other_f = other.cost + other.heuristic
        return self_f < other_f
        
    def from_string(string: str) -> State:
        lines = string.strip().splitlines()
        return State(list(
            map(lambda x: list(x.strip()), lines)
        ))




#################
# Problem class #
#################
class PageCollect(Problem):
    """
    The PageCollect class, extending the Problem class, defines a pathfinding problem where a student has to collect pages
    in a maze before bringing them all to the examiner.

    Attributes
    ----------
    goal_pos (int): tuple of int (x, y) describing the goal's coordinates
    """
    def __init__(self, initial: State) -> None:
        """
        Initializes the goal state using the initial state's grid, then initializes the PageCollect problem using the
        initial and goal states

        Arguments
        ---------
        initial: State instance representing the initial state of the problem
        """
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
        goal = State(final_goal, 0, 0, self.goal_pos, 0, [])
        super().__init__(initial, goal=goal)

    def actions(self, state: State) -> list:
        """
        Returns the list of possible actions for the student in a given specific state

        Arguments
        ---------
        state: State instance representing the current state the problem is in

        Returns
        -------
        A list of strings depicting in which of the four direction (N, S, E, W) the student can currently go
        """
        acts = []
        grid = state.grid
        player_x, player_y = state.player_pos
        if grid[player_y+1][player_x] != "#":
            acts.append("s")
        if grid[player_y-1][player_x] != "#":
            acts.append("n")
        if grid[player_y][player_x+1] != "#":
            acts.append("e")
        if grid[player_y][player_x-1] != "#":
            acts.append("w")
        return acts

    
    def result(self, state: State, action: str) -> State:
        """
        Returns a new State instance representing in which state the problem will be next when applying an action to the
        current state

        Arguments
        ---------
        state: State instance representing the current state the problem is in
        action: str indicating in which direction the student will move next

        Returns
        -------
        A new State instance corresponding to the previous one with an additional move from the student, with updated pages
        if necessary
        """
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

        new_state = State(grid, state.cost+1, 0, (new_x, new_y), n_pages, pages_pos)
        new_state.heuristic = h(new_state, self.goal_pos)
        return new_state

    def goal_test(self, state: State) -> bool:
        return state == self.goal
    
    def h(self, node: Node) -> int:
        """
        The h function returns the heuristic value corresponding to a node given the final goal

        Arguments
        ---------
        node: a Node instance to compute the heuristic value of

        Returns
        -------
        A heuristic value computed by using the sum of the manhattan distances to each page, or to the goal if there
        are no more pages to collect
        """
        h = 0
        if (node.state.n_pages !=0):
            for i in range(node.state.n_pages):
                h += dist_man(node.state.player_pos,node.state.pages_pos[i])
        else:
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

# Example of search
node = astar_search(problem)

# example of print
path = node.path()

for n in path:
    print(n.state)  # assuming that the __str__ function of state outputs the correct format
    print()
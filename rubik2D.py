"""
Name of the author(s):
- Louis Navarre <louis.navarre@uclouvain.be>
"""
import time
import sys
from search import *


#################
# Problem class #
#################
class Rubik2D(Problem):

    def actions(self, state):
        pass

    def result(self, state, action):
        #if action not in self.actions(state) :
        #    print("action not valid")
        #    return
        if action[0] == "right":
            return self.moveRight(state, action[1], action[2])
        if action[0] == "down":
            return self.moveDown(state, action[1], action[2])

    def goal_test(self, state):
        return state.goal == state.grid

    def moveRight(self, state, row, dec):
        """
        :param state: instance à modifier
        :param row: indice de la ligne a modifier
        :param dec: nombre de case a decaler
        :return: instance state modifiée
        """
        toMove = list(state.grid)
        r = list(state.grid[row])
        end = r[-dec::]
        del r[-dec::]
        r = tuple(end + r)
        toMove[row] = r
        state.grid = tuple(toMove)
        state.move += "Row #" + str(row) + " down " + str(dec)
        return state


    def moveDown(self, state, col, dec):
        """
        :param state: instance du rubik cube
        :param col: indice de la colonne a changer
        :param dec: nombre de cases a decaler
        :return: l'instance modifiee
        """
        toMove = list(state.grid)
        Col = []
        for l in toMove:
            Col.append(l[col])

        end = Col[-dec::]
        del Col[-dec::]
        Col = end + Col

        for i in range(len(toMove)):
            l = list(toMove[i])
            l[col] = Col[i]
            toMove[i] = tuple(l)

        state.grid = tuple(toMove)
        state.move += "Col #" + str(col) + " down " + str(dec)
        return state

###############
# State class #
###############
class State:

    def __init__(self, shape, grid, answer=None, move="Init"):
        self.shape = shape # taille de la grille
        self.answer = answer
        self.grid = grid # etat
        self.move = move # ordre des moves

    def __str__(self):
        s = self.move + "\n"
        for line in self.grid:
            s += "".join(line) + "\n"
        return s


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

def breadth_first_tree_search(problem):
    pass
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: ./rubik2D.py <path_to_instance_file>")
    filepath = sys.argv[1]

    shape, initial_grid, goal_grid = read_instance_file(filepath)
    print(shape)
    print(initial_grid)
    print(goal_grid)
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

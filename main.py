# A maze generator and solver implemented with
# Depth-First Search, Randomized Prim and A* search
# 2021-09-19

import os, shutil
from Maze.algorithms import *


if __name__ == '__main__':

    # 0 - View settings
    # 1 - Depth-first search
    # 2 - Prim
    algorithm = 1

    # clean up previous output
    if os.path.isdir(CAPDIR):
        shutil.rmtree(CAPDIR)

    # clean up the terminal
    os.system("clear")

    mainloop(algorithm)



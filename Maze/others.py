from algorithms import *

# Subroutine for A star with decoloring

def run_astar(frame):
    '''Subroutine to run A star'''

    maze = frame.maze

    start = maze.nodes[0].current  #top left
    end = maze.nodes[-1].current   #bottom right

    current = start
    visited, path = [start], deque([start])

    visited, path = astar(maze, start, current, end, visited, path)
    print('astar returned visited, path')
    print(f'visited :: len, {len(visited)}\n{visited}')
    print(f'path :: len, {len(path)}\n{path}')


    len_path = len(path)
    render_path = []

    for i in range(len_path - 1):
        render_path.append([path[i], path[i+1]])


    cur_f = 0    # initialize frame
    max_frames = len(render_path) + 1
    path_frame = render_path[:cur_f]

    decolor_factor = (n*(n-1))/2   # number of iterations in which the color would be modified
    DECOLOR_1 = 255
    DECOLOR_1_MIN = 0
    DECOLOR_2 = 0
    DECOLOR_2_MAX = 255

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # sys.stdout.write('\r')
        # # sys.stdout.write('Current frame: %d/%d' % (cur + 1, c_max))
        # sys.stdout.flush()
        screen.fill(BG_SCREEN)
        show_message('SOLVING')
        draw_maze_nodes(frame)

        for node in path_frame:
            draw_corridor(node[0], node[1], (DECOLOR_1, DECOLOR_2, 30))
            DECOLOR_1 -= abs(DECOLOR_1 - DECOLOR_1_MIN) / decolor_factor
            DECOLOR_2 += abs(DECOLOR_2 - DECOLOR_2_MAX) /decolor_factor

        pygame.display.update()
        # pygame.image.save(screen, './capture/path_%04d.tga' % (cur + 1))
        clock.tick(FPS//2)

        cur_f += 1  # update frame
        if cur_f == max_frames:
            print('\n')
            return
        else:
            path_frame = render_path[:cur_f]

# backup run A star

def run_astar(frame):
    '''Subroutine to run A star'''

    maze = frame.maze

    start = maze.nodes[0].current  #top left
    end = maze.nodes[-1].current   #bottom right

    current = start
    visited, path = [start], deque([start])

    visited, path = astar(maze, start, current, end, visited, path)
    print('astar returned visited, path')
    print(f'visited :: len, {len(visited)}\n{visited}')
    print(f'path :: len, {len(path)}\n{path}')

    len_path = len(path)
    render_path = []

    for i in range(len_path - 1):
        render_path.append([path[i], path[i+1]])

    cur_f = 0    # initialize frame
    max_frames = len(render_path) + 1
    path_frame = render_path[:cur_f]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # sys.stdout.write('\r')
        # # sys.stdout.write('Current frame: %d/%d' % (cur + 1, c_max))
        # sys.stdout.flush()
        screen.fill(BG_SCREEN)
        show_message('SOLVING')
        draw_maze_nodes(frame)

        for node in path_frame:
            draw_corridor(node[0], node[1], PATH_color)

        pygame.display.update()
        # pygame.image.save(screen, './capture/path_%04d.tga' % (cur + 1))
        clock.tick(FPS//2)

        cur_f += 1  # update frame
        if cur_f == max_frames:
            print('\n')
            return
        else:
            path_frame = render_path[:cur_f]

# color palettes
# BG_color = (22, 5, 3)
# CORRIDOR_Color = (58, 159, 41)
# HEAD_color = (241, 109, 59)
# TEXT_color = (255, 255, 255)
# TEXT_BOX_color = (20, 20, 20)
# PATH_color = (150,50,50)

# BG_color = (0, 0, 0)
# CORRIDOR_Color = (252, 255, 0)
# HEAD_color = (241, 109, 59)
# TEXT_color = (255, 255, 255)
# TEXT_BOX_color = (20, 20, 20)
# PATH_color = (0, 60, 37)


# Subroutine for implementing maze generators
# 2021-09-07

from Maze.structs import *
import sys
import random
import pygame
from pygame.locals import *
from itertools import product
from copy import deepcopy
from collections import deque

CELLSIZE = 20
X_CELLS = 18  # number of horizontal cells
Y_CELLS = 18  # number of vertical cells

FPS = 30  # speed of visualization

PYGAMEWIDTH = CELLSIZE * X_CELLS
PYGAMEHEIGHT = CELLSIZE * Y_CELLS
PYGAMEHEIGHT_TITLE = PYGAMEHEIGHT + 2 * CELLSIZE  # extra space at bottom to render text

X_GRID = (range(0, PYGAMEWIDTH, CELLSIZE))
Y_GRID = (range(0, PYGAMEHEIGHT, CELLSIZE))

SIZESQ = 0.6 * CELLSIZE  # size of each segment to be render
OFFSET = 0.5 * SIZESQ  # offset from the center
PAUSETIME_END = int(10e3)
PAUSETIME_MIDDLE = int(10e2)

BG_color = (17, 0, 15)
CORRIDOR_Color = (206, 0, 178)
HEAD_color = (0, 250, 246)
TEXT_color = (0, 250, 246)
TEXT_BOX_color = (20, 20, 20)
PATH_color = (255, 138, 0)

# running options

ALG_FUNC = {0: 'view_settings()', 1: 'run_DFS()', 2: 'run_prim()'}
ALG_TITLE = {0: f'Grid setting ({X_CELLS} + {Y_CELLS})', 1: 'Depth-First Search', 2: 'Prims Algorithm'}


# ----- Subroutines for rendering objects -----

def in_canvas(vect):
    '''Check if an Vector instance is inside the range of canvas.'''

    X_inside = (0 < vect.x < MAZEWIDTH)
    Y_inside = (0 < vect.y < MAZEHEIGHT)

    return X_inside and Y_inside


def possible_neighbors(vect):
    '''enumerates valid possible neighbors of a Vector.'''

    N_1 = Vector(vect.x + CELLSIZE, vect.y)
    N_2 = Vector(vect.x - CELLSIZE, vect.y)
    N_3 = Vector(vect.x, vect.y + CELLSIZE)
    N_4 = Vector(vect.x, vect.y - CELLSIZE)

    return list(filter(in_canvas, [N_1, N_2, N_3, N_4]))


def draw_centers():
    """Subroutine for displaying the grid setting."""

    for X, Y in product(X_GRID, Y_GRID):
        x, y = X + CELLSIZE // 2, Y + CELLSIZE // 2
        pygame.draw.rect(screen, (58, 159, 41), (x - OFFSET, y - OFFSET, SIZESQ, SIZESQ))


def draw_corridor(cell_1, cell_2, color=CORRIDOR_Color):
    '''draw a corridor connecting two cells.'''

    x_positions = [cell_1.x, 0.5 * (cell_1.x + cell_2.x), cell_2.x]
    y_positions = [cell_1.y, 0.5 * (cell_1.y + cell_2.y), cell_2.y]

    for X, Y in zip(x_positions, y_positions):
        corridor = pygame.Rect(X - OFFSET, Y - OFFSET, SIZESQ, SIZESQ)
        pygame.draw.rect(screen, color, corridor)


def in_draw_referent(node):
    '''Finds AAAAAACCCCCCCAAAAAAAAAAA
    '''

    x_cell, y_cell = node.current.x, node.current.y
    x_grid, y_grid = x_cell - CELLSIZE // 2, y_cell - CELLSIZE // 2

    x_index, y_index = X_GRID.index(x_grid), Y_GRID.index(y_grid)

    return (x_index + y_index) % 2


def draw_maze_nodes(frame):
    '''Render the current status of a maze by drawing channels
    between connected nodes on a frame.'''

    drawing_nodes = [node for node in frame.maze.nodes if in_draw_referent(node)]

    for node in drawing_nodes:
        for neighbor in node.neighbors:
            draw_corridor(node.current, neighbor)

    X, Y = frame.head.x, frame.head.y
    head = pygame.Rect(X - OFFSET, Y - OFFSET, SIZESQ, SIZESQ)
    pygame.draw.rect(screen, HEAD_color, head)


def show_message(message: str, display=False, size: int = 20, color=TEXT_color):
    '''Subroutine for displaying a message.'''

    font = pygame.font.Font('ARCADECLASSIC.ttf', size)
    title_text = font.render(message, True, color, TEXT_BOX_color)
    text_rect = title_text.get_rect()

    text_box = pygame.Rect(CELLSIZE / 4, MAZEHEIGHT, MAZEWIDTH - CELLSIZE / 2, 2 * CELLSIZE - 6)
    pygame.draw.rect(screen, TEXT_BOX_color, text_box)
    screen.blit(title_text, (MAZEWIDTH / 2 - text_rect.width / 2, MAZEHEIGHT + 4))

    if display:
        pygame.display.update()


def show_coloring_message(message: str, iterations: int, current: int, size: int = 20, GREEN_1=0):
    '''Subroutine for displaying a message.'''

    current = current + 1

    GREEN_MAX = 255
    GREEN = GREEN_1 + (GREEN_MAX / (iterations - 1)) * current

    font = pygame.font.Font('ARCADECLASSIC.ttf', size)
    title_text = font.render(message, True, (255, GREEN, 0), TEXT_BOX_color)
    text_rect = title_text.get_rect()

    text_box = pygame.Rect(CELLSIZE / 4, MAZEHEIGHT, MAZEWIDTH - CELLSIZE / 2, 2 * CELLSIZE - 6)
    pygame.draw.rect(screen, TEXT_BOX_color, text_box)
    screen.blit(title_text, (MAZEWIDTH / 2 - text_rect.width / 2, MAZEHEIGHT + 4))


# ----- Subroutines for controlling gameflow -----

def view_settings():
    '''Subroutine for displaying grid settings without
    running algorithms.'''

    resolution = (MAZEWIDTH, MAZEHEIGHT)

    pygame.init()
    screen = pygame.display.set_mode(resolution, DOUBLEBUF)
    pygame.display.set_caption(ALG_TITLE[0])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen.fill(BG_SCREEN)
        draw_centers()

        pygame.display.update()

        pygame.time.delay(PAUSETIME_END)
        pygame.quit()
        sys.exit()


def mainloop(algorithm):
    '''Subroutine for running algorithms'''

    resolution = (MAZEWIDTH, PYGAMEHEIGHT_TITLE)
    global clock, screen

    pygame.init()
    screen = pygame.display.set_mode(resolution, DOUBLEBUF)
    pygame.display.set_caption(ALG_TITLE[algorithm])
    clock = pygame.time.Clock()

    while True:
        # os.mkdir(CAPDIR) ##############
        last_frame = eval(ALG_FUNC[algorithm])

        if last_frame:
            show_message('Searching way out', True)
            pygame.time.delay(PAUSETIME_MIDDLE)
            run_astar(last_frame)
            show_message('SOLVED !!!', True)

        pygame.time.delay(PAUSETIME_END)
        pygame.quit()
        sys.exit()


def create_maze():
    '''Subroutine for creating a maze with its nodes.'''

    print('Creating maze...')
    maze = Maze()

    for X, Y in product(X_GRID, Y_GRID):
        cell_x, cell_y = X + CELLSIZE // 2, Y + CELLSIZE // 2
        current = Vector(cell_x, cell_y)
        neighbors = []
        maze.insert_node(Node(current, neighbors))

    print(f'Maze size: {MAZEWIDTH} * {MAZEHEIGHT}')
    return maze


# ----- Subroutines for algorithms -----

def dfs(start, maze, unvisited, frames):
    '''Subroutine for creating the maze recursively and marking
    each connected node.'''

    if unvisited == []:
        return frames

    neighbors = [N for N in possible_neighbors(start)]
    random.shuffle(neighbors)

    for new_start in neighbors:
        if maze.is_visited(new_start):
            continue
        else:
            maze.set_connected(start, new_start)
            maze.set_visited(new_start)
            unvisited.remove(new_start)
            frames.append(Frame(new_start, deepcopy(maze)))
            is_full = dfs(new_start, maze, unvisited, frames)
            if is_full:
                return is_full
            else:
                continue


def run_DFS():
    '''Subroutine for creating a maze and run depth-first search.'''

    maze = create_maze()
    unvisited = [node.current for node in maze.nodes]

    start = random.choice(unvisited)
    maze.set_visited(start)
    unvisited.remove(start)

    frames = [Frame(start, deepcopy(maze))]

    print('Generating frames... this might take a few seconds')
    frames = dfs(start, maze, unvisited, frames)

    cur_f = 0  # initialize frame
    max_frames = len(frames)
    current_frame = frames[cur_f]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen.fill(BG_SCREEN)

        draw_maze_nodes(current_frame)

        show_coloring_message('CREATING MAZE', max_frames, cur_f, 25)

        pygame.display.update()
        clock.tick(FPS)

        cur_f += 1

        if cur_f == max_frames:
            print(current_frame)
            return current_frame
        else:
            current_frame = frames[cur_f]


def prim(maze):
    unvisited = [node.current for node in maze.nodes]
    heads = []  # cells heading the expansion
    frames = []

    start_x = random.choice(X_GRID) + CELLSIZE // 2
    start_y = random.choice(Y_GRID) + CELLSIZE // 2
    start = Vector(start_x, start_y)

    maze.set_visited(start)
    heads.append(start)
    unvisited.remove(start)

    frames.append(Frame(start, deepcopy(maze)))

    while unvisited != []:
        head = random.choice(heads)
        neighbors = possible_neighbors(head)
        random.shuffle(neighbors)
        for neighbor in neighbors:
            if not maze.is_visited(neighbor):
                maze.set_visited(neighbor)
                heads.append(neighbor)
                unvisited.remove(neighbor)
                maze.set_connected(head, neighbor)
                frames.append(Frame(neighbor, deepcopy(maze)))
                break  # don't continue with the others heads neighbors

    print(frames[-1])
    return frames


def run_prim():
    maze = create_maze()

    print('Generating frames. This will take a wile...')
    frames = prim(maze)

    cur_f = 0  # initialize frame
    max_frames = len(frames)
    current_frame = frames[cur_f]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen.fill(BG_SCREEN)
        draw_maze_nodes(current_frame)
        show_message('CREATING MAZE')

        pygame.display.update()
        clock.tick(FPS)

        cur_f += 1

        if cur_f == max_frames:
            print(current_frame)
            return current_frame
        else:
            current_frame = frames[cur_f]


# ----- A* Search -----

def manhattan(vect_1, vect_2):
    '''Calcultates the estimate cost of the path from vect_1
    to vect_2, with only four directions permitted.'''

    x_dist = abs(vect_2.x - vect_1.x)
    y_dist = abs(vect_2.y - vect_1.y)

    return (x_dist + y_dist)


def astar(maze, start, current, end, visited, path):
    '''Subroutine to apply A star algorithm to find the maze path.'''

    if current == end:
        # print('astar finish --- if current == end: return visited, path')
        # print(f'visited ::\n{visited}')
        # print(f'path ::\n{path}')
        return visited, path

    choices = [C for C in maze.get_neighbors(current) if C not in visited]

    choices.sort(key=lambda c: manhattan(start, c))
    choices.sort(key=lambda c: manhattan(c, end))

    for next_move in choices:

        visited.append(next_move)
        path.append(next_move)
        visited_final, path_final = astar(maze, start, next_move, end, visited, path)

        if path_final is not None:
            return visited_final, path_final
        else:
            path.pop()

    return visited, None


def run_astar(frame):
    '''Subroutine to run A star'''

    maze = frame.maze

    start = maze.nodes[0].current  # top left
    end = maze.nodes[-1].current  # bottom right

    current = start
    visited, path = [start], deque([start])

    visited, path = astar(maze, start, current, end, visited, path)
    # print('astar returned visited, path')
    # print(f'visited :: len, {len(visited)}\n{visited}')
    # print(f'path :: len, {len(path)}\n{path}')

    len_path = len(path)
    render_path = []

    for i in range(len_path - 1):
        render_path.append([path[i], path[i + 1]])

    print(f'render_path:: {render_path}')

    cur_f = 0  # initialize frame
    max_frames = len(render_path) + 1
    path_frame = render_path[:cur_f]

    coloring_factor = (len_path * (len_path - 1)) / 2  # number of iterations in which the color would be modified
    RED = 255
    RED_min = 0
    GREEN = 0
    GREEN_max = 255

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # sys.stdout.write('\r')
        # # sys.stdout.write('Current frame: %d/%d' % (cur + 1, c_max))
        # sys.stdout.flush()
        screen.fill(BG_SCREEN)
        show_message('SOLVING')
        draw_maze_nodes(frame)

        for node in path_frame:
            draw_corridor(node[0], node[1], (RED, GREEN, 35))
            RED -= abs(RED - RED_min) / coloring_factor
            GREEN += abs(GREEN - GREEN_max) / coloring_factor

        pygame.display.update()
        # pygame.image.save(screen, './capture/path_%04d.tga' % (cur + 1))
        clock.tick(FPS // 2)

        cur_f += 1  # update frame
        if cur_f == max_frames:
            print('\n')
            return
        else:
            path_frame = render_path[:cur_f]



















# Data Structures for implementing algorithms
# 2021-09-19

from dataclasses import *


@dataclass
class Vector:
    """Two-dimensional vector to represent nodes.
    >> v = Vector(0, 1)
    >> v
    Vector(x=0, y=1)
    """
    x: int
    y: int

    def copy(self):
        '''Return a copy a vector.
        >> v = Vector(1, 2)
        >> w = v.copy()
        >> v is w
        False
        '''
        self_type = type(self)
        return self_type(self.x, self.y)

    def __iadd__(self, other):
        '''v.__iadd__(w) -> v += w
        >> v = Vector(1, 2)
        >> w = Vector(1, 1)
        >> v += w
        >> v
        Vector(x=2, y=3)
        >> v += 2
        >> v
        Vector(x=4, y=5)
        '''
        if isinstance(other, Vector):
            self.x += other.x
            self.y += other.y
        else:
            self.x += other
            self.y += other
        return self

    def __add__(self, other):
        '''v.__add__(w) -> v + w
        >> v = Vector(2, 1)
        >> w = Vector(1, 1)
        >> v + w
        >> v
        Vector(x=3, y=2)
        >> v + 2
        >> v
        Vector(x=5, y=4)
        '''
        copy = self.copy()
        return copy.__iadd__(other)


@dataclass
class Node:
    """Data Structure for representing each node."""
    # neighbors are mutable, current inmutable

    visited = False
    current: Vector
    neighbors: list = field(default_factory=list)

    def add_neighbor(self, target):
        # add instances of Vector to neighbors
        if not isinstance(target, Vector):
            print (f'Cannot add {target}, its not a Vector')
        elif target in self.neighbors:
            print(f'{target} already in neighbors')
        else:
            self.neighbors.append(target)


@dataclass
class Maze:
    '''Data Structure containing all nodes.'''
    nodes: list = field(default_factory=list)

    def insert_node(self, target):
        # add instances of Node to Maze
        if not isinstance(target, Node):
            print(f'Cannot add {target}, its not a Node')
        elif target in self.nodes:
            print(f'{target} already in Maze nodes')
        else:
            self.nodes.append(target)

    def is_visited(self, vect):
        # given a vect, check if a node is visited
        for node in self.nodes:
            if node.current == vect:
                return node.visited
        print('Node not found')

    def set_visited(self, vect):
        # given a vect operates on a node to set as visited
        found = False
        for i, node in enumerate(self.nodes):
            if node.current == vect:
                self.nodes[i].visited = True
                found = True
        if found is False:
            print('Node not found')

    def has_node(self, vect):
        # given a vect return the Node instance
        vectors = [node.current for node in self.nodes]
        return vect in vectors

    def set_connected(self, vect_1, vect_2):
        # given vect operate on node
        assert self.has_node(vect_1) and self.has_node(vect_2), 'At least one not found'

        for i, node in enumerate(self.nodes):
            if node.current == vect_1:
                self.nodes[i].add_neighbor(vect_2)
            elif node.current == vect_2:
                self.nodes[i].add_neighbor(vect_1)

    def get_neighbors(self, target):
        # finds a nodes connected neighbors
        for node in self.nodes:
            if node.current == target:
                return node.neighbors
        print('Node not found')

    def __str__(self):
        str_nodes = 'Maze:\n'
        for node in self.nodes:
            str_nodes += str(node) + '\n'
        return str_nodes

@dataclass
class Frame:

    head: Vector     # cell leading the generation
    maze: Maze       # current status of maze

    def __str__(self):
        return f'Frame: \nHead: {self.head} \n{self.maze}'

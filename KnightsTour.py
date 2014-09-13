#!/usr/bin/env python3

from pprint import pprint

class KnightsTour(object):
  '''
  The Knight's Tour is a puzzle consisting of
  a standard 8x8 chess board and a single Knight.

  Traditionally the knight begins in the upper left
  corner.  The goal is to find the minimum number of
  moves for the knight to visit every square on the
  board, along with providing its path.

  The KnightsTour class treats the chess board as
  a graph where a node is a square and an edge exists
  between two squares if the knight can move from one
  to the other.  The graph implementation follows Guido's 
  representation as found:

    https://www.python.org/doc/essays/graphs/

  Given the graph, the goal is to find a path covering
  every node at most once, i.e., no cycles are allowed.

  Nodes are implemented with 2-tuples as follows:

  (0,0) == a8
  (0,1) == b8
      ...
  (7,7) == h1

  Where a8, b8, etc. are standard chess board positions.
  This scheme applies in the same way to any other size
  board.
  '''
  def __init__(self, start=(0,0), size=8):
    '''
    Construct a KnightMoves object.

    Parameters
    ----------
    start : 2-tuple (int, int)
      Starting location for the knight
      Defaults to (0,0), i.e., a8, i.e.,
      the upper left corner

    size : int
      Size of the square board to use
      Defaults to a standard 8x8 board
    '''
    # Save the customizable starting place and size
    self.start = start
    self.size = size

    # Build the graph
    self.graph = { (i, j) : self.moves((i, j)) \
                    for i in range(self.size)  \
                    for j in range(self.size) 
                 }

  def moves(self, square):
    '''
    Return a list of all the squares that the knight
    can reach in a single move from the square passed
    in.

    Parameters
    ----------
    square : 2-tuple (int, int)
      Square the knight is currently on, i.e., where to
      return moves from
    '''
    x, y = square
  
    # Left two up one; left two down one
    left_twos = [(x - 2, y - 1), (x - 2, y + 1)] 

    # Right two up one; right two down one
    right_twos = [(x + 2, y - 1), (x + 2, y + 1)]

    # Up two left one; up two right one
    up_twos = [(x - 1, y - 2), (x + 1, y - 2)]

    # Down two left one; down two right one
    down_twos = [(x - 1, y + 2), (x + 1, y + 2)]

    all_moves = left_twos + right_twos + up_twos + down_twos
    return [move for move in all_moves if self.valid(move)]

  def valid(self, square):
    '''
    Return True if square is a valid 2-tuple for the
    board used by self.

    Parameters
    ----------
    square : 2-tuple (int, int)
      Square the knight is currently on, i.e., where to
      return moves from
    '''
    x, y = square
    return (0 <= x < self.size) and (0 <= y < self.size)

  def findTour(self):
    '''
    Return a list of a path for the knight to take which
    covers each square exactly once.
    '''
    return self._findPath(self.start)

  def _findPath(self, start, path=[]):
    '''
    Called by the findTour method.  Not meant to be called
    publicly.

    This function is a modified version of a backtracking
    path finding algorithm given by Guido in his essay about
    representing graphs in Python.

    Parameters
    ----------
    start : 2-tuple (int, int)
      Starting location for the current path being explored

    path : [(int, int)] 
      List of squares to take in the knight's shortest tour
    '''
    # Add the starting node to the path being explored
    path = path + [start]

    # If the path list contains all the squares, we're done
    if len(path) == self.size**2:
      return path

    # Warnsdorff's Rule: (Heuristic)
    # Explore first the move with fewest next moves
    nodes = [node for node in self.graph[start] if node not in path]
    for node in sorted(nodes, key=lambda x: len(self.graph[x])):
      # Only add nodes not currently in the path list
      # since we only want each square to appear once
      if node not in path:
        newpath = self._findPath(node, path)
        if newpath:
          return newpath

    # If we've gone through every node that's reachable
    # from the start and haven't found a complete path, 
    # give up on this path
    return None

  def printBorder(self, width):
    for _ in range(self.size):
      print('+{}'.format('-' * width), end='') 

    print('+')

  def printPath(self, path):
    order = { square : path.index(square) + 1 for square in path }
    width = len(str(self.size**2)) + 2 # Width of each square printed

    for n in range(1, self.size**2 + 1):
      square = ((n-1) // self.size, (n-1) % self.size)
      if (n - 1) % self.size == 0:
        if (n - 1) != 0: print('|')
        self.printBorder(width)

      print('|{:^{}}'.format(order[square], width), end='')

    if n != 0: print('|')
    self.printBorder(width)

if __name__ == '__main__':
  kt = KnightsTour()
  tour = kt.findTour()
  kt.printPath(tour)

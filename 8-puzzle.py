# Course: CS325 - Analysis of Algorithms
# Student Name: Calvin Lam
# Assignment: Portfolio Assignment
# Description: Implementation of the n-Puzzle problem (# 12) from 'A Survey of
#              NP-Complete puzzles'. The game is played on an (m x m) grid
#              where (m**2 - 1 = n) and within the grid exists n square
#              tiles label 1 ... n. There exists 1 'blank' tile that can be
#              moved up, down, left, or right depending on the current
#              position. The board is set to a random configuration and this
#              blank tile is used to swap positions with other numbered
#              tiles until a 'goal' configuration is reached.
#              A* heuristic search reference: https://youtu.be/wJu3IZq1NFs


import random


class Grid:
    """
    Class to represent the playing grid of size (3 x 3)
    """
    def __init__(self, f_n, g_n, parent, children, grid=None):
        self.grid = grid
        self.goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.f_n = f_n
        self.g_n = g_n
        self.parent = parent
        self.children = children

    def set_f_n(self):
        """f(n) = g(n) + h(n)"""
        self.f_n = self.get_h_n() + self.g_n

    def get_h_n(self):
        """h(n) = number of misplaced tiles compared to the goal grid"""
        h_n = 0
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] != self.goal[i][j]:
                    h_n += 1
        return h_n

    def randomize_grid(self):
        """Randomize grid state and instantiate in self.grid"""
        rand_digit = []
        for digit in range(9):
            rand_digit.append(digit)
        random.shuffle(rand_digit)

        idx = 0
        new_list = []
        while idx < len(rand_digit):
            new_list.append(rand_digit[idx:idx + 3])
            idx += 3
        self.grid = new_list

    def visualize_grid(self):
        """More readable print method of grid data"""
        for row in self.grid:
            print(*row)

    def find_blank(self):
        """Find the blank '0' tile from the grid"""
        row_index = 0
        for row in self.grid:
            if 0 in row:
                return [row_index, row.index(0)]
            row_index += 1

    def set_children(self):
        """Function to find children of a given grid"""
        # Start with blank tile
        row, col = self.find_blank()

        # Possible directions include Up, Down, Left, Right
        directions = [[row, col - 1], [row, col + 1], [row - 1, col],
                      [row + 1, col]]
        children_list = []
        # Attempt to make_move in all 4 directions, create and store a child
        # for each legal move
        for d in directions:
            child = self.make_move(row, col, d[0], d[1])
            if child:
                temp = Grid(0, self.g_n + 1, self, None, child)
                children_list.append(temp)
        self.children = children_list

    def make_move(self, start_r, start_c, end_r, end_c):
        """Function to move the blank tile in a given direction"""
        # First create a copy to avoid mutating the original
        grid = []
        for r in self.grid:
            col = []
            for c in r:
                col.append(c)
            grid.append(col)

        # If the move is within legal range
        if 0 <= end_r <= 2 and 0 <= end_c <= 2:
            # In place swap
            temp = grid[end_r][end_c]
            grid[end_r][end_c] = grid[start_r][start_c]
            grid[start_r][start_c] = temp
            return grid
        else:
            return None


class Puzzle:
    """
    Class to represent the 8-puzzle game instance
    """
    def __init__(self):
        self.open = []
        self.closed = []

    @staticmethod
    def is_solvable(grid):
        """Check if a given grid is solvable based on the rule that solvable
        boards contain an even number of inversions """
        # Flatten out list of list into singular list to simplify
        flat = []
        for i in range(3):
            for j in range(3):
                flat.append(grid[i][j])

        # Count number of inversions where inversion is a lower index number
        # being larger than a later index number
        counter = 0
        for x in range(9):
            for y in range(x + 1, 9):
                if flat[x] > flat[y] > 0:
                    counter += 1
        if counter % 2 == 0:
            return counter
        return False

    @staticmethod
    def verification(grid, goal):
        """Verification method to see if a given grid state has reached the
        goal state"""
        for i in range(3):
            for j in range(3):
                if grid[i][j] != goal[i][j]:
                    return False
        return True

    def puzzle_loop(self):
        """Primary loop for user puzzle game"""
        # First user choice
        # 1) User input their own starting grid
        # 2) Randomly generate starting grid
        # Instantiate a random non-solvable graph to enter while loop
        start = Grid(0, 0, None, None, [[2, 1, 0], [0, 0, 0], [0, 0, 0]])
        solvable = self.is_solvable(start.grid)
        while not solvable:
            choice_1 = input('Press "1" to input your own starting grid\n'
                             'Press "2" to randomly generate a starting grid: '
                             )

            if choice_1 == '1':
                user_grid = []
                print('\nPlease input a starting grid of the format\n'
                      '# # #\n'
                      '# # #\n'
                      '# # #\n'
                      'With # being digits 0-8 and "0" represents the blank '
                      'tile:\n')
                for i in range(3):
                    temp = input().split(' ')
                    user_grid.append(temp)
                # Convert str input to int
                for i in range(3):
                    for j in range(3):
                        user_grid[i][j] = int(user_grid[i][j])
                start.grid = user_grid

            if choice_1 == '2':
                print('\nCreating randomized starting grid...')
                start.randomize_grid()

            # Verify if the user input OR randomized grid is solvable
            print('\nVerifying if the puzzle is solvable...')
            solvable = self.is_solvable(start.grid)
            if solvable:
                print('Yes -- this puzzle is solvable!\n')
            else:
                print('No -- this puzzle is NOT solvable.\n')

        # Once a solvable grid has been established (randomly or via input)
        # Second user choice
        print('Here is the current state of the graph:\n')
        start.visualize_grid()
        print('')

        # Begin with the starting grid in the open list
        self.open.append(start)
        # Open list = unprocessed children
        # Closed list = all children processed
        solved = False
        while not solved:
            # User choose input VS automated solution
            print('Would you like to solve the puzzle yourself?')
            choice_2 = input('Press "1" to try solving yourself\n'
                             'Press "2" for the auto solver: ')

            if choice_2 == '1':
                curr = self.open[0]
                while curr.get_h_n() != 0:
                    # Locate '0' tile
                    x, y = curr.find_blank()

                    # Make move using based on one of four input directions
                    direct = input('\nPlease choose a direction to move the '
                                   'blank: ')
                    if direct == 'up':
                        curr.grid = curr.make_move(x, y, x-1, y)
                        curr.visualize_grid()
                    if direct == 'down':
                        curr.grid = curr.make_move(x, y, x+1, y)
                        curr.visualize_grid()
                    if direct == 'left':
                        curr.grid = curr.make_move(x, y, x, y-1)
                        curr.visualize_grid()
                    if direct == 'right':
                        curr.grid = curr.make_move(x, y, x, y+1)
                        curr.visualize_grid()

                    check = input('Would you like to verify your solution? ('
                                  'y/n)')
                    if check == 'y':
                        if self.verification(curr.grid, curr.goal):
                            print('The goal has been achieved!')
                        else:
                            print('The goal has NOT been reached, please '
                                  'continue')
                    if check == 'n':
                        pass
                solved = True

            if choice_2 == '2':
                while True:
                    curr = self.open[0]
                    # If h(n), the difference between curr and goal,
                    # is 0 this means the goal has been reached
                    if curr.get_h_n() == 0:
                        parent_queue = [curr]
                        while curr.parent is not None:
                            parent_queue.append(curr.parent)
                            curr = curr.parent

                        # Print formatting to visually display steps taken
                        # and total number of steps in the solver solution
                        step_count = 0
                        for grid in reversed(parent_queue):
                            print("Step " + str(step_count) + ":")
                            grid.visualize_grid()
                            print("--------------------")
                            step_count += 1
                        print("\nTotal steps = " + str(step_count - 1))
                        break

                    # Instantiate children via set_children()
                    curr.set_children()

                    for i in curr.children:
                        # Instantiate f_n and append to open
                        i.set_f_n()
                        if i.grid not in self.closed:
                            self.open.append(i)
                    # Curr is now fully explored and now append to closed
                    self.closed.append(curr.grid)
                    del self.open[0]

                    # Sort the list such that lowest f(n) is now open[0]
                    self.open.sort(key=lambda var: var.f_n)
                solved = True


# Primary driver code
p = Puzzle()
p.puzzle_loop()

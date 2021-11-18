# 8-Puzzle-Solver

n-Puzzle, also known as a sliding puzzle, is played on a (nxn) grid with m number of tiles where m = n^2 - 1 ensuring that there is always exactly 1 blank tile.
The objective is to move tiles around until a defined 'goal state' is reached. This 8-Puzzle-Solver primarily focuses on the (3x3) grid and allows users to:

1) Either generate their own starting (3x3) grid or have one automatically generated
2) Check to see if the generated grid in step 1 is solvable before moving to step 3
3) Give users the choice to solve the grid manually or have the program automatically solve
4) If manually solving, the user can choose to move the blank either Up, Down, Left, or Right while staying within the (3x3) boundary

Once the goal state is reached successfully the program will display the path and number of steps taken.
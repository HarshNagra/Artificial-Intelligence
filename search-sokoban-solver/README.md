# Search - Sokoban Solver

The goal of this project is to implement a working solver for the puzzle game Sokoban shown in figure below. Sokoban is a puzzle game in which a warehouse robot must push boxes into storage spaces. The rules hold that only one box can be moved at a time, that boxes can only be pushed by a robot and not pulled, and that neither robots nor boxes can pass through obstacles (walls or other boxes). In addition, robots cannot push more than one box, i.e., if there are two boxes in a row, the robot cannot push them. The game is over when all the boxes are in their storage spots.

In this version of Sokoban the rules are slightly more complicated, as there may be more than one warehouse robot available to push boxes. These robots cannot pass through one another nor can they move simultaneously.

## Test Results

##### Testing Manhattan Distance
In the problem set provided, you calculated the correct Manhattan distance for 20 states out of 20.
States that were incorrect: []

##### Testing alternate heuristic with best_first search
Of 20 initial problems, 15 were solved in less than 8 seconds by this solver.
Problems that remain unsolved in the set are Problems: [5, 9, 17, 18, 19]
The benchmark implementation solved 12 out of 20 practice problems given 8 seconds.

##### Testing fval_function
Test 0 calculated fval: 6.0 correct: 6
Test 1 calculated fval: 11.0 correct: 11
Test 2 calculated fval: 16.0 correct: 16

Your fval_function calculated the correct fval for 3 out of 3 tests.

##### Testing Anytime GBFS
Of 20 initial problems, 15 were solved in less than 8 seconds by this solver.
Of the 15 problems that were solved, the cost of 15 matched or outperformed the benchmark.
Problems that remain unsolved in the set are Problems: [5, 9, 17, 18, 19]
The benchmark implementation solved 12 out of the 20 practice problems given 8 seconds.

##### Testing Anytime Weighted A Star
Of 20 initial problems, 13 were solved in less than 8 seconds by this solver.
Of the 13 problems that were solved, the cost of 13 matched or outperformed the benchmark.
Problems that remain unsolved in the set are Problems: [5, 9, 15, 16, 17, 18, 19]
The benchmark implementation solved 12 out of the 20 practice problems given 8 seconds.
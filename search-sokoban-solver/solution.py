#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

import os #for time functions
from search import * #for search engines
from sokoban import SokobanState, Direction, PROBLEMS #for Sokoban specific classes and problems
import itertools


def sokoban_goal_state(state):
  '''
  @return: Whether all boxes are stored.
  '''
  for box in state.boxes:
    if box not in state.storage:
      return False
  return True

def heur_manhattan_distance(state):
#IMPLEMENT
    '''admissible sokoban puzzle heuristic: manhattan distance'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #We want an admissible heuristic, which is an optimistic heuristic.
    #It must never overestimate the cost to get from the current state to the goal.
    #The sum of the Manhattan distances between each box that has yet to be stored and the storage point nearest to it is such a heuristic.
    #When calculating distances, assume there are no obstacles on the grid.
    #You should implement this heuristic function exactly, even if it is tempting to improve it.
    #Your function should return a numeric value; this is the estimate of the distance to the goal.
    
    sum = 0
    for box in state.boxes:
        maximum = float("inf") # greatest number
        for storage in state.storage:
            (xStorage, yStorage) = storage # retrieving coordinates
            (xBoxCor, yBoxCor) = box  # retrieving coordinates
            distancex = abs(xBoxCor - xStorage) 
            distancey = abs(yBoxCor - yStorage)
            if (distancex+distancey) < maximum:
                maximum = distancex+distancey #total movement between
        sum = (sum+maximum)
    return sum #manhattan distance


#SOKOBAN HEURISTICS
def trivial_heuristic(state):
    '''trivial admissible sokoban heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state (# of moves required to get) to the goal.'''
    count = 0
    for box in state.boxes:
        if box not in state.storage:
            count += 1
    return count

def heur_alternate(state):
#IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #heur_manhattan_distance has flaws.
    #Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    #Your function should return a numeric value for the estimate of the distance to the goal.
    
    # Checks for states that are not possible

    for box in state.boxes:
        if box not in storageSpaces(box,state):
          # (1) Corner - Box is placed in the corner, therefore, cant move
            if checkCorner(box, state): 
              return float("inf")
          # (2) Edge - the Box is on the edge, and no storage touching that edge
            if checkEdge(box,state): 
              return float("inf")

    # Two Parts
    # Robot to the box
    # Box to the storage
    
    return robotAndBox(state) + boxAndStorage(state)


#### Helper Functions

def robotAndBox(state):
  minimum = float("inf")
  possibilities = [list(zip(state.robots, p)) for p in itertools.permutations(state.boxes)]

  for possibility in possibilities:
    distance = 0
    for robotToBox in possibility:
        ((xRobCor, yRobCor), (xBoxCor, yBoxCor)) = robotToBox
        distance += (abs(xRobCor - xBoxCor) + abs(yRobCor - yBoxCor)) - 1

    #replacing minimum at every comparison
    if minimum > distance:
        minimum = distance

  return minimum
    
def boxAndStorage(state):
    
    minimum = float("inf")
    pair = None

    permutations = [list(zip(state.boxes, p)) for p in itertools.permutations(state.storage)]

    # From Box position to storage

    for possibility in permutations:
        sum = 0
        for boxToStorage in possibility:
            ((xBoxCor, yBoxCor), (xStoCor, yStoCor)) = boxToStorage
            sum +=  abs(xBoxCor - xStoCor) + abs(yBoxCor - yStoCor)

        if sum < minimum:
            pair = possibility
            minimum = sum
    
    # When the box and storage are on the edge
    move = 0
    for boxToStorage in pair:
        ((xBoxCor, yBoxCor), (xStoCor, yStoCor)) = boxToStorage

        if (xBoxCor, yBoxCor) == (xStoCor, yStoCor):

            upDown = False
            leftRight = False

            if leftRight != True:
                to = (state.height - xBoxCor + 1)
                for i in range(1, to):
                    if (xBoxCor + i, yBoxCor) not in state.storage:
                        break
                    else:
                        leftRight = True
                        minimum = minimum + 1
                if leftRight:
                    move = move - 1

            if leftRight != True:
                to = (-yBoxCor - 1)
                for i in range(-1, to, -1):
                    if (xBoxCor + i, yBoxCor) not in state.storage:
                        break
                    else: 
                        minimum = minimum + 1
                        leftRight = True
                if leftRight:
                    move = move - 1
            
            if upDown != True:
                to = (-yBoxCor - 1)
                for i in range(-1, to, -1):
                    if (xBoxCor, yBoxCor + i) not in state.storage:
                        break
                    else:
                        minimum = minimum + 1
                        upDown = True
                if upDown:
                    move = move - 1

            if upDown != True:
                to = (state.height - yBoxCor + 1)
                for i in range(1, to):
                    if (xBoxCor, yBoxCor + i) not in state.storage:
                        break
                    else:
                        minimum = minimum + 1
                        upDown = True
                if upDown:
                    move = move - 1

    minimum = minimum + move

    return minimum



def storageSpaces(box, state):
    # To make a list all the available storage places
    empty = []
    # all storage spaces
    for storage in state.storage:
        empty.append(storage)
    # box already in empty space, saves time
    if box in empty:
        temp = []
        temp.append(box)
        return temp
    # storage space occupied by the other boxes
    for notCurrentBox in state.boxes:
        if (notCurrentBox != box) and (notCurrentBox in empty):
            empty.remove(notCurrentBox)
    return empty

def checkCorner(position,state):
    x = position[0]
    y = position[1]
   
    obstacleAndBoxes = state.obstacles|state.boxes

    if x == state.width-1:
        if y == 0 or y == state.height-1:
            return True
        if (x,y+1) in obstacleAndBoxes or (x,y-1) in obstacleAndBoxes:
            return True
        return False

    if x==0:
        if y == 0 or y == state.height - 1:
            return True
        if (x,y-1) in obstacleAndBoxes or (x,y+1) in obstacleAndBoxes:
            return True
        return False
    

    #obstacles around the box

    if (x,y+1) in state.obstacles:
        if (x-1,y) in state.obstacles or (x+1,y) in state.obstacles:
            return True

    if (x,y-1) in state.obstacles:
        if (x-1,y) in state.obstacles or (x+1,y) in state.obstacles: 
            return True

    return False
    
def checkEdge(position,state):
   
    saveAvailableStorage = storageSpaces(position,state)
    xSave = []
    ySave = []

    for (x, y) in saveAvailableStorage:
        xSave.append(x)
        ySave.append(y)
    if position[0] == 0:
        if 0 not in xSave: 
            return True
    if position[0]== (state.width-1):
        if (state.width-1) not in xSave: 
            return True
    if position[1]== 0:
        if 0 not in ySave: 
            return True
    if position[1]==(state.height-1):
        if (state.height-1) not in ySave: 
            return True
    
    return False

### EXTRA OVER

def heur_zero(state):
    '''Zero Heuristic can be used to make A* search perform uniform cost search'''
    return 0

def fval_function(sN, weight):
#IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
  
    #Many searches will explore nodes (or states) that are ordered by their f-value.
    #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    #The function must return a numeric f-value.
    #The value will determine your state's position on the Frontier list during a 'custom' search.
    #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    return (weight * sN.hval) + sN.gval 

def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound = 10):
#IMPLEMENT
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of weighted astar algorithm'''

    time_remaining = timebound
    se = SearchEngine('custom', 'full')
    fval_wrap = (lambda sN: fval_function(sN, weight))
    se.init_search(initial_state, sokoban_goal_state, heur_fn, fval_wrap)
    best_solution = float("inf")

    start_time = os.times()[0]
    result = se.search(time_remaining,costbound=(float("inf"),float("inf"),best_solution))
    end_time = os.times()[0]

    time_remaining = time_remaining - (end_time - start_time)
    
    if result : 
        best_solution = result.gval + heur_fn(result)   
    else:
        return False

    while time_remaining > 0 and not se.open.empty():
            start_time = os.times()[0]
            better_result = se.search(time_remaining,(float("inf"),float("inf"),best_solution))
            end_time = os.times()[0]
            time_remaining = time_remaining - (end_time - start_time)
            if better_result:
                best_solution = better_result.gval + heur_fn(better_result)
                result = better_result
            else:
                break

    return result
  

def anytime_gbfs(initial_state, heur_fn, timebound = 10):
    #IMPLEMENT
    '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of weighted astar algorithm'''
    time_remaining = timebound

    se = SearchEngine('best_first', 'full')
    se.init_search(initial_state, sokoban_goal_state, heur_fn)
    best_solution = float("inf")

    start_time = os.times()[0]
    result = se.search(time_remaining, costbound=(best_solution,float("inf"),float("inf")))
    end_time = os.times()[0]

    time_remaining = time_remaining - (end_time - start_time)

    if result :
        best_solution = result.gval 
    else:
        return False

    while time_remaining > 0 and not se.open.empty():
            start_timex = os.times()[0]
            better_result = se.search(time_remaining,(best_solution,float("inf"),float("inf")))
            end_timex= os.times()[0]
            time_remaining = time_remaining - (end_timex - start_timex)
            if better_result:
                best_solution = better_result.gval
                result = better_result
            else:
                break
    
    return result



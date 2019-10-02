# A* for Sliding Puzzle

# Import packages
import numpy as np
import queue

# Define global variables
goalState = np.array(
        [[0,1,2],
         [3,4,5],
         [6,7,8]])
initState = np.loadtxt('mp1input.txt', dtype=np.int)

def main():
    # Implement A* Algorithm
    frontier = queue.PriorityQueue() # maintain set of states being analyzed
    startState = PuzzState() # initial state instance
    frontier.put(startState)
    
    closedSet = set() # aka "Explored Set"
    explrdStates = 1 # variable to keep track of explored states
    while not frontier.empty():
        nextState = frontier.get() # retrieve lowest fcost-state as determined by __lt__
        savedState = np.copy(nextState.puzz) # create copy of state being explored for expansion
        
        # Check if it's the goal state (i.e. check state for expansion)
        if nextState.is_goal():
            nextState.show_path() # method to show the path used to get to the goal state
            break # exit the loop
            
        # Add next state to the closed set
        closedSet.add(nextState)

        # Expand all the states where move is possible & ignore those already visited
        possibleMoves = ['up', 'down', 'left', 'right'] # list of possible moves
        for move in possibleMoves:
            if nextState.can_move(move): # determine if move is allowed
                neighbor = nextState.gen_nextState(move, savedState) # create neighboring state instance resulting from given direction
                if neighbor in closedSet: # determine the neighboring state has already been visited
                    continue # ignore if previously visited
                if neighbor not in frontier.queue:
                    frontier.put(neighbor) # add state to the frontier
                    explrdStates += 1 # increment explored states
    print('\nNumber of states visited =',explrdStates)
        
class PuzzState(): # class object to store all state attributes
    START = np.unravel_index(initState.argmin(),initState.shape) # tuple of starting coordinates for 0

    def __init__(self, curConfig=initState, zero=START, g=0, f=0, predState=None, action_from_pred=None):
        self.puzz = np.copy(curConfig)
        self.zeroCoords = zero
        self.gcost = g # path cost
        self.fcost = f # estimated cost of the cheapest solution
        self.pred = predState
        self.action_from_pred = action_from_pred

    def __str__(self):
        a = np.array(self.puzz) # create copy of the puzzle
        return np.str(a)
        
    def __eq__(self, other): # check if 2 states are equal
        return np.all(self.puzz == other.puzz) 
    
    def __lt__(self, other): # compares f-costs & reprioritize in queue
        return self.fcost < other.fcost 

    def __hash__(self): # hash function for managing closed set
        return self.zeroCoords.__hash__()   
    
    def is_goal(self): # check if a goal state is reached
        return np.all(self.puzz == goalState)
        
    def can_move(self, direction): # determine if 0-sqr can move in certain direction
        if direction=='up':
            coords = (self.zeroCoords[0]-1, self.zeroCoords[1])
        elif direction=='down':
            coords = (self.zeroCoords[0]+1, self.zeroCoords[1])
        elif direction=='left':
            coords = (self.zeroCoords[0], self.zeroCoords[1]-1)
        elif direction=='right':
            coords = (self.zeroCoords[0], self.zeroCoords[1]+1)
        else:
            raise('wrong direction for checking move')
        
        # Check if new coords created are valid (i.e. within bounds of puzzle)
        if coords[0]<0 or coords[0]>=self.puzz.shape[0] or coords[1]<0 or coords[1]>=self.puzz.shape[1]:
            return False
        else:
            return True

    # Generate the state(s) which result from 0-sqr's allowable moves
    def gen_nextState(self, direction, savedState):
        #  Create new state instance
        s = PuzzState(savedState, tuple(self.zeroCoords), self.gcost, self.fcost, self)
        
        # Return coordinates of move based on chosen direction
        if direction=='up': 
            coords = (self.zeroCoords[0]-1, self.zeroCoords[1])
            swapNum = self.puzz.item(coords)
        elif direction=='down':
            coords = (self.zeroCoords[0]+1, self.zeroCoords[1])
            swapNum = self.puzz.item(coords)
        elif direction=='left':
            coords = (self.zeroCoords[0], self.zeroCoords[1]-1)
            swapNum = self.puzz.item(coords)
        elif direction=='right':
            coords = (self.zeroCoords[0], self.zeroCoords[1]+1)
            swapNum = self.puzz.item(coords)
        else:
            raise('wrong direction for checking move')
       
        # Perform swap
        s.puzz[[self.zeroCoords[0]], [self.zeroCoords[1]]] = swapNum
        s.puzz[[coords[0]], [coords[1]]] = 0
        
        # Update instance attributes
        s.gcost += 1
        s.zeroCoords = coords
        s.action_from_pred = direction

        h = 0
        for i in range(1,10):
            h += np.sum(np.abs(np.argwhere(s.puzz==i) - np.argwhere(goalState==i)))
        s.fcost = h + s.gcost
        
        return s
    
    # Perform look-back on all pred states & print from start-to-finish
    move = 0 # variable to count how many moves were taken
    def show_path(self): 
        if self.pred is not None:
            self.pred.show_path()
        
        # Print move number & action to get to that state
        if PuzzState.move==0:
            print('START')
        else:
            print('Move', PuzzState.move, 'ACTION', self.action_from_pred)
            
        PuzzState.move = PuzzState.move + 1
        print(self)

if __name__ == "__main__":
    main()
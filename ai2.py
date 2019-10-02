# Tic Tac Toe AI - Variable Board Size

# Import packages
import numpy as np

# Initiate variables
LOST = 0
WON = 1
DRAW = 2
boardSize = int(input("Please enter the size of the board n (e.g. n=3,4,5,...): "))

def main():

    # Create the game board of the given size
    board = GenGameBoard(boardSize)
            
    board.printBoard()  # Print the board before starting the game loop
            
    # Game loop
    while True:
        # *** Player's move ***        
        
        # Try to make the move and check if it was possible
        # If not possible get col,row inputs from player    
        row, col = -1, -1 # TS added - for boolean check within makeMove()
        while not board.makeMove(row, col, 'X'):
            print("Player's Move")
            row, col = input("Choose your move (row, column): ").split(',')
            row = int(row)
            col = int(col)
#            row, col = 1 , 1 # HARDCODE for now
    
        # Display the board again
        board.printBoard()
                
        # Check for ending condition
        # If game is over, check if player won and end the game
        if board.checkWin('X'): # i.e. if checkWin returns True
            # Player won
            result = WON
            break
        elif board.noMoreMoves(): # i.e. if noMoreMoves returns True
            # No moves left -> draw
            result = DRAW
            break
                
        # *** Computer's move ***
        board.makeCompMove()
        
        # Print out the board again
        board.printBoard()    
        
        # Check for ending condition
        # If game is over, check if computer won and end the game
        if board.checkWin('O'):
            # Computer won
            result = LOST
            break
        elif board.noMoreMoves():
            # No moves left -> draw
            result = DRAW
            break
            
    # Check the game result and print out the appropriate message
    print("GAME OVER")
    if result==WON:
        print("You Won!")            
    elif result==LOST:
        print("You Lost!")
    else: 
        print("It was a draw!")

# self class is responsible for representing the game board
class GenGameBoard: 
    
    def __init__(self, boardSize):
        self.boardSize = boardSize
        self.marks = np.empty((boardSize, boardSize),dtype='str')
        self.marks[:,:] = ' '
    
    # Prints the game board using current marks
    def printBoard(self): 
        # Prthe column numbers
        print(' ',end='')
        for j in range(self.boardSize):
            print(" "+str(j+1), end='')
        
        
        # Prthe rows with marks
        print("")
        for i in range(self.boardSize):
            # Prthe line separating the row
            print(" ",end='')
            for j in range(self.boardSize):
                print("--",end='')
            
            print("-")

            # Prthe row number
            print(i+1,end='')
            
            # Prthe marks on self row
            for j in range(self.boardSize):
                print("|"+self.marks[i][j],end='')
            
            print("|")
                
        
        # Prthe line separating the last row
        print(" ",end='')
        for j in range(self.boardSize):
            print("--",end='')
        
        print("-")
    
    
    # Attempts to make a move given the row,col and mark
    # If move cannot be made, returns False and prints a message if mark is 'X'
    # Otherwise, returns True
    def makeMove(self, row, col, mark):
        possible = False  # Variable to hold the return value
        if row == -1 and col == -1:
            return False
        
        # Change the row,col entries to array indexes
        row = row - 1
        col = col - 1
        
        if row<0 or row>=self.boardSize or col<0 or col>=self.boardSize:
            print("Not a valid row or column!")
            return False
        
        # Check row and col, and make sure space is empty
        # If empty, set the position to the mark and change possible to True
        if self.marks[row][col] == ' ':
            self.marks[row][col] = mark # place X in coords provided
            possible = True # break while loop (i.e. move is valid and complete)
        
        # Print-out the message to the player if the move was not possible
        if not possible and mark=='X': # i.e. if possible==False and mark=='X'
            print("\nself position is already taken!")
        
        return possible
    
    # Determines whether a game winning condition exists
    # If so, returns True, and False otherwise
    def checkWin(self, mark):
        won = False # Variable holding the return value
        
        # Check wins by examining each combination of positions
        
        # Check each row
        for i in range(self.boardSize):
            won = True
            for j in range(self.boardSize):
                if self.marks[i][j]!=mark:
                    won=False
                    break        
            if won:
                break
        
        # Check each column
        if not won:
            for i in range(self.boardSize):
                won = True
                for j in range(self.boardSize):
                    if self.marks[j][i]!=mark:
                        won=False
                        break
                if won:
                    break

        # Check first diagonal
        if not won:
            for i in range(self.boardSize):
                won = True
                if self.marks[i][i]!=mark:
                    won=False
                    break
                
        # Check second diagonal
        if not won:
            for i in range(self.boardSize):
                won = True
                if self.marks[self.boardSize-1-i][i]!=mark:
                    won=False
                    break

        return won
    
    # Determines whether the board is full
    # If full, returns True, and False otherwise
    def noMoreMoves(self):
        return (self.marks!=' ').all() # returns True if all indices in array are filled; False otherwise
    
    def isXturn(self): # returns True if X's turn to move, false otherwise
        return np.count_nonzero(self.marks == 'X') == np.count_nonzero(self.marks == 'O')
    
    def possibleMoves(self):
        possibleMoves = []
        for x,i in enumerate(self.marks):
            for y,j in enumerate(i):
                if j == ' ':
                    possibleMoves.append([x,y])
        return possibleMoves
    
    def checkUtil(self, mark):
        if self.checkWin(mark):
            if mark == 'X':
                return -1
            elif mark == 'O':
                return 1
        if self.noMoreMoves():
            return 0 # draw
    
    def max_value(self, alpha, beta): # O-player
        mark = 'X' if self.isXturn() else 'O' # determine player's mark
        oMark = 'O' if self.isXturn() else 'X' # determine opponent's mark
        
        # If current board is in game ending state,
        # return the utility to computer player
        if self.noMoreMoves() or self.checkWin(oMark): # terminal check
            utilVal = self.checkUtil(oMark)
            return utilVal, None
        
        v = -float("inf")
        
        # Go through all possible marks that can be made
        for move in self.possibleMoves():
            row = move[0]
            col = move[1]
            self.marks[row][col] = mark # make current move (mark) on board

            minVal = self.min_value(alpha, beta) # recursive minimax search
            if minVal[0] > v: # update best value for given node
                v = minVal[0]
                best_move = move # coordinates to achieve highest minimax value
            self.marks[row][col] = ' ' # backtrack to prior state
            
            # Alpha-Beta Pruning
            if v >= beta:
                return v, best_move
            alpha = max(alpha, v)
        return v, best_move

    def min_value(self, alpha, beta): # X-player
        mark = 'X' if self.isXturn() else 'O' # determine player's mark
        oMark = 'O' if self.isXturn() else 'X' # determine opponent's mark
        
        # If current board is in game ending state,
        # return the utility to computer player
        if self.noMoreMoves() or self.checkWin(oMark): # terminal check
            utilVal = self.checkUtil(oMark)
            return utilVal, None
        
        v = float("inf")
        
        # Go through all possible marks that can be made
        for move in self.possibleMoves():
            row = move[0]
            col = move[1]
            self.marks[row][col] = mark # make current move (mark) on board
            maxVal = self.max_value(alpha, beta) # recursive minimax search
            if maxVal[0] < v: # update best value for given node
                v = maxVal[0]
            self.marks[row][col] = ' ' # backtrack to prior state
            
            # Alpha-Beta Pruning
            if v <= alpha:
                return v, None
            beta = min(beta, v)
        return v, None
    
    # Return best move for computer
    def getBest(self):
        alpha = -float("inf")
        beta = float("inf")
        return self.max_value(alpha, beta)
    
    # Then make best move for the computer by placing the mark in the best spot
    def makeCompMove(self):
        
        # Initiate alpha beta search
        best_move = self.getBest()[1]
        row = best_move[0]
        col = best_move[1]
        self.marks[row][col] = 'O'
        print("Computer chose: "+str(row+1)+","+str(col+1))
        
if __name__ == "__main__":
    main()
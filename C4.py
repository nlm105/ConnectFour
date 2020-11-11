import random
import numpy as np
import copy
import json


##########################################
# Board class
##########################################

class Board:

    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # Constructor. Declares 10x10 game board array.
    #    Board is left to right, from top to bottom. 0-9 is first row,
    #    10-19 second, 20-29 third, etc
    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    def __init__(self):

        # Declare char array
        self.gameboard = np.empty((100), dtype='U')

        # Header row of invalid char
        for i in range(0, 10):
            self.gameboard[i] = 'e'  # 'e' denotes invalid

        # Gameboard columns and sentinel nodes
        for i in range(10, 90):
            if (i % 10 == 0):
                self.gameboard[i] = 'e'  # 'e' denotes invalid
            elif (i % 10 == 9):
                self.gameboard[i] = 'e'  # 'e' denotes invalid
            else:
                self.gameboard[i] = ' '

        # Tail row of invalid char
        for i in range(90, 100):
            self.gameboard[i] = 'e'  # 'e' denotes invalid

        # Initialize movecounter
        self.movecounter = 0

        # Intialize columnheight. Posn 0 is unused.
        # Posn 1-8 corresponds to how many moves placed in a particular column.
        self.columnheight = np.empty((9), dtype=int)
        for i in range(0, 9):
            self.columnheight[i] = 0

    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # Draw the board
    # You will have to change this for your project
    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    def draw(self):

        # Draws the grid by printing a blank line,
        # the line with a character, and another blank line.
        # If not the last row in the grid, prints a separation line between rows.
        # formatting so that the draw method looks good.

        for i in range(10, 90, 10):
            print(self.gameboard[i + 1], self.gameboard[i + 2], self.gameboard[i + 3], self.gameboard[i + 4],
                  self.gameboard[i + 5], self.gameboard[i + 6], self.gameboard[i + 7], self.gameboard[i + 8])
        print("1 2 3 4 5 6 7 8")

    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # Checks the position of the array, returns it
    #   returns blank, X, or O. Can return 'e' for sentinel value
    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    def checkPosn(self, posn):
        if (posn < 100):
            return self.gameboard[posn]
        return 'e'  # sentinel value (invalid)

    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # Full move-playing system, semi-auto.
    # Updates gameboard, and redraws the grid
    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    def makeMove(self, player, position):
        self.update(player, position)
        self.draw()

        # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # Changes a position on the game board array to the
    # current player's character.
    # Called by makeMove
    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    def update(self, player, column):

        # Find row by taking 80 (max row) and subtracting by 10*columnheight
        posn = 80 - (10 * self.columnheight[column])

        # Move posn to correct column by adding "column"
        posn = posn + column

        self.gameboard[posn] = player  # could be CPU or User
        self.movecounter = self.movecounter + 1
        self.columnheight[column] = self.columnheight[column] + 1

    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # Checks the legality of a move by ensuring that the column was not full
    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    def isLegal(self, column):
        return (self.columnheight[column] < 8)


##########################################
# ConnectFour
##########################################

class ConnectFour:

    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # Constructor with first move.
    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    def __init__(self, diffX, diffO):
        self.diffO = diffO
        self.diffX = diffX
        self.Grid = Board()

    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # returns True if X move, False if O
    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    def whoseMove(self):
        # if number of moves made is even then it is X's turn
        return ((self.Grid.movecounter % 2) == 0)

    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # returns the best move that X can make
    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    def bestMoveX(self, lookahead):
        Xposn = 0
        bestXvalue = -1000

        decvalues = np.empty((9), dtype=int)  # in order to choose a random move

        # Filling with -100
        for i in range(0, 9):
            decvalues[i] = -1000

        # Looping through all possible moves
        for i in range(1, 9):

            # Clearing any previous simulation moves
            # copyGame = ConnectFour(self)
            copyGame = copy.deepcopy(self)

            # Checking if position is valid
            if (copyGame.Grid.isLegal(i)):
                copyGame.Grid.update('X', i)
                decisionvalue = self.bestGuess(copyGame, lookahead, -10, 10)
                # print(self.whoseMove(), " ", i, " ", decisionvalue)

                # If decisionvalue is better than bestvalue,
                #    then posn = i, and bestvalue = decisionvalue for this iteration
                decvalues[i] = decisionvalue
                if (decisionvalue > bestXvalue):
                    Xposn = i
                    bestXvalue = decisionvalue

        # loop checking all possible moves
        choice = random.randint(1, 8)
        while (True):
            if (decvalues[choice] == bestXvalue):
                return choice
            choice = (choice + 1) % 8

    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # returns the best move that O can make
    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    def bestMoveO(self, lookahead):
        Oposn = 0
        bestOvalue = 1000

        decvalues = np.array(9)  # in order to choose a random move

        # Filling with -1000
        for i in range(0, 9):
            decvalues[i] = -1000

        # Looping through all possible moves
        for i in range(1, 9):

            # Clearing any previous simulation moves
            # copyGame = ConnectFour(self)
            copyGame = copy.deepcopy(self)

            # Checking if position is valid
            if (copyGame.Grid.isLegal(i)):
                copyGame.Grid.update('O', i)
                decisionvalue = self.bestGuess(copyGame, lookahead, -10, 10)
                # print(self.whoseMove(), " ", i, " ", decisionvalue)

                # If decisionvalue is better than bestvalue,
                #    then posn = i, and bestvalue = decisionvalue for this iteration
                decvalues[i] = decisionvalue
                if (decisionvalue < bestOvalue):
                    Oposn = i
                    bestOvalue = decisionvalue

        # if the move was legal
        # loop checking all possible moves
        choice = random.randint(1, 8)
        while (True):
            if (decvalues[choice] == bestOvalue):
                return choice
            choice = (choice + 1) % 8

    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # Uses difficulty level to simulate moves to find best possible move
    #    for the computer. Each level of simulationvalue is one full recursive
    #    simulation.
    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    def bestGuess(self, game, simlevel, a, b):

        # End of simulation if simlevel = 0 or movecounter >= 64.
        # This is as far as the computer will or can look forward.
        result = self.judge(game.Grid)
        if (simlevel == 0 or game.Grid.movecounter >= 64 or result == -10 or result == 10):
            if (result == 0):
                return result
            elif (result == 10):
                return (10)
            else:
                return (-10)

        # Determine whose turn
        if (game.whoseMove()):  # X's move
            maxval = -9999

            # Looping through all moves. Calling bestguess on all moves.
            for i in range(1, 9):

                if (game.Grid.isLegal(i)):
                    # copyGame = ConnectFour(game)
                    copyGame = copy.deepcopy(game)
                    copyGame.Grid.update('X', i)
                    testval = self.bestGuess(copyGame, simlevel - 1, a, b)

                    # Checking testval against maxval, reassigning if necessary
                    if (testval > maxval):
                        maxval = testval

                    if testval > a:
                        a = testval

                    if (a >= b):
                        break

            return maxval

        else:  # O's move
            # Tracking WorstValue
            minval = 9999

            # Looping through all moves. Calling bestguess on all moves.
            for i in range(1, 9):

                # Legality check
                if (game.Grid.isLegal(i)):
                    # copyGame = ConnectFour(game)
                    copyGame = copy.deepcopy(game)
                    copyGame.Grid.update('O', i)
                    testval = self.bestGuess(copyGame, simlevel - 1, a, b)

                    # Checking testval against maxval, reassigning if necessary
                    if (testval < minval):
                        minval = testval

                        if testval < b:
                            b = testval
                        if (b <= a):
                            break

            return minval

            # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # returns how good the game is from the X standpoint
    #    ongoing game: 0.    X win:  10.    O win: -10
    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    def judge(self, game):

        # Checks each posn for player characters. If no char found, posn ignored.
        for i in range(11, 90):
            if (game.checkPosn(i) == "X"):

                # All checks assume that posn is on leftmost (or topmost)
                # side of win cond.

                # Vertical Win cond. Fills testing chars, if possible.
                # If not possible, continues with other win conds.
                try:
                    a = game.checkPosn(i)
                    b = game.checkPosn(i + 10)
                    c = game.checkPosn(i + 20)
                    d = game.checkPosn(i + 30)
                    if (b == a and c == a and d == a):
                        return 10

                except e:
                    # Do nothing. Error thrown means that this went out of
                    # bounds and no win condition is possible.
                    a = a

                    # Horizontal Win Condition. Same methodology as vertical.
                try:
                    a = game.checkPosn(i)
                    b = game.checkPosn(i + 1)
                    c = game.checkPosn(i + 2)
                    d = game.checkPosn(i + 3)
                    if (b == a and c == a and d == a):
                        return 10

                except e:
                    # Do nothing. Error thrown means that this went out of
                    # bounds and no win condition is possible.
                    a = a

                    # Downward Diagonal Win Condition
                try:
                    a = game.checkPosn(i)
                    b = game.checkPosn(i + 9)
                    c = game.checkPosn(i + 18)
                    d = game.checkPosn(i + 27)
                    if (b == a and c == a and d == a):
                        return 10

                except e:
                    # Do nothing. Error thrown means that this went out of
                    # bounds and no win condition is possible.
                    a = a

                    # Upward Diagnonal Win Condition
                try:
                    a = game.checkPosn(i)
                    b = game.checkPosn(i + 11)
                    c = game.checkPosn(i + 22)
                    d = game.checkPosn(i + 33)
                    if (b == a and c == a and d == a):
                        return 10

                except e:
                    # Do nothing. Error thrown means that this went out of
                    # bounds and no win condition is possible.
                    a = a

                    # End player checks

            elif (game.checkPosn(i) == "O"):
                # All checks assume that posn is on leftmost (or topmost)
                # side of win cond.

                # Vertical Win cond. Fills testing chars, if possible.
                # If not possible, continues with other win conds.
                try:
                    a = game.checkPosn(i)
                    b = game.checkPosn(i + 10)
                    c = game.checkPosn(i + 20)
                    d = game.checkPosn(i + 30)
                    if (b == a and c == a and d == a):
                        return -10

                except e:
                    # Do nothing. Error thrown means that this went out of
                    # bounds and no win condition is possible.
                    a = a

                    # Horizontal Win Condition. Same methodology as vertical.
                try:
                    a = game.checkPosn(i)
                    b = game.checkPosn(i + 1)
                    c = game.checkPosn(i + 2)
                    d = game.checkPosn(i + 3)
                    if (b == a and c == a and d == a):
                        return -10

                except e:
                    # Do nothing. Error thrown means that this went out of
                    # bounds and no win condition is possible.
                    a = a

                    # Upward Diagonal Win Condition
                try:
                    a = game.checkPosn(i)
                    b = game.checkPosn(i + 9)
                    c = game.checkPosn(i + 18)
                    d = game.checkPosn(i + 27)
                    if (b == a and c == a and d == a):
                        return -10

                except e:
                    # Do nothing. Error thrown means that this went out of
                    # bounds and no win condition is possible.
                    a = a

                    # Downward Diagnonal Win Condition
                try:
                    a = game.checkPosn(i)
                    b = game.checkPosn(i + 11)
                    c = game.checkPosn(i + 22)
                    d = game.checkPosn(i + 33)
                    if (b == a and c == a and d == a):
                        return -10

                except e:
                    # Do nothing. Error thrown means that this went out of
                    # bounds and no win condition is possible.
                    a = a

                    # End CPU checks

            # End Char checking loop

        # No win conditions
        return 0

    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # Player move
    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    def Xmove(self):
        # self.Grid.draw()
        self.Grid.makeMove('X', self.bestMoveX(self.diffX))

        # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # Computer makes move
    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    def Omove(self):
        # self.Grid.makeMove('O', self.bestMoveO(self.diffO))
        print("Please enter your move: ")
        self.Grid.makeMove('O', int(input()))
    # Omove


###########################################
# Main
###########################################

# Note:  X always moves first

# set the lookahead in the range 0..7
difficultyX = random.randint(0, 7)
difficultyO = random.randint(0, 7)

# create a ConnectFour game
game = ConnectFour(difficultyX, difficultyO)

outputX = []
outputO = []

winner = ""

def changeLoser(arr):
    for i in arr:
        i[1] = i[1]*-1


# While game is not finished, loop continuously
while (game.Grid.movecounter < 64 and game.judge(game.Grid) == 0):

    # True for X move, false for O move
    if (game.whoseMove()):
        game.Xmove()
        outputX.append([game.Grid.gameboard.tolist(), game.Grid.movecounter])
    else:
        game.Omove()
        outputO.append([game.Grid.gameboard.tolist(), game.Grid.movecounter])

    # Find winner and print result.
    # 10 = X win, 0 = draw, -10 = O win
    result = game.judge(game.Grid)

    if (result == -10):
        print("O wins")
        winner = "O"
    elif (result == 0):
        print("Draw")
    elif (result == 10):
        print("X wins")
        winner = "X"
    else:
        print("Unreachable State - Error")

    print("Lookahead: X=", difficultyX)
    print("Lookahead: O=", difficultyO)


totalTurns = game.Grid.movecounter
print(totalTurns)

if winner == "O":
    changeLoser(outputX)
elif winner == "X":
    changeLoser(outputO)


print(outputX)
print(outputO)
with open('X.json', 'w') as outfile:
    json.dump(outputX, outfile)

with open('O.json', 'w') as outfile:
    json.dump(outputO, outfile)

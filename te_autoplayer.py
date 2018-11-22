''' Implement an AI to play tetris '''
from random import Random
from te_settings import Direction
import random

current = 19
numToRotate = 0
posToMoveTo = -1
newGame = True


# newGame = True

class AutoPlayer():
    """ A very simple dumb AutoPlayer controller """

    def __init__(self, controller):
        global numToRotate, current, posToMoveTo
        self.controller = controller
        self.rand = Random()
        current = 19
        numToRotate = 0
        posToMoveTo = -1

    def next_move(self, gamestate):
        global numToRotate, inProgress, current, posToMoveTo, newGame
        ''' next_move() is called by the game, once per move.
            gamestate supplies access to all the state needed to autoplay the game.'''
        if self.isRowEmpty(gamestate.get_tiles()[19]) == True:
            # print("new game")
            current = 19
            numToRotate = 0
            posToMoveTo = -1
            inProgress = False
            newGame = True

        self.call_next(gamestate)

    def toPosition(self, gamestate, position):

        if (position < gamestate.get_falling_block_position()[0]):
            gamestate.move(Direction.LEFT)
        elif (position > gamestate.get_falling_block_position()[0]):
            gamestate.move(Direction.RIGHT)

    def cloneMoveToPosition(self, clone, position):
        while position != clone.get_falling_block_position()[0]:
            # clone.print_block_tiles()
            # print("moving")
            # print(position)
            # print(clone.get_falling_block_position()[0])
            self.toPosition(clone, self.get_pos_to_move(clone, position))
            clone.update()

    def getNext(self, list, value):
        i = 0
        for x in list:
            if x == value:
                return i
            i += 1
        return i

    def getNextSkip(self, list, value, startAfter):
        i = 0
        for x in list:
            if x == value and i > startAfter:
                return i
            i += 1
        return i

    def isRowEmpty(self, list):
        i = 0
        for x in list:
            if x != 0:
                return False
            i += 1
        return True

    def getBlockBottomStart(self, gamestate):
        listLen = len(gamestate.get_falling_block_tiles())
        i = 1
        lastEmpty = -1
        for x in gamestate.get_falling_block_tiles():
            if self.getNext(x, 1) == listLen:
                lastEmpty = i
            i += 1

        if lastEmpty == -1:
            return gamestate.get_falling_block_tiles()[listLen - 1]
        return gamestate.get_falling_block_tiles()[lastEmpty - 2]

    def getBlockWidth(self, gamestate):
        pos = 0
        for x in gamestate.get_falling_block_tiles():
            count = 0
            for i in x:
                if i == 1:
                    if count > pos:
                        pos = count  # update largest block exist
                count += 1
        return pos

    def get_pos_to_move(self, gamestate, position):
        global current

        blockBottomStart = self.getNext( self.getBlockBottomStart(gamestate), 1)
        if blockBottomStart == len(gamestate.get_falling_block_tiles()):
            blockBottomStart = 0

        posToMove = position - blockBottomStart

        if position + self.getBlockWidth(gamestate) > 9:
            # print("Bigger case!!!")
            posToMove = position - (position + self.getBlockWidth(gamestate) - 9)

        return posToMove

    def getRowScore(self, clone, rowNum):
        lastEmpty = False
        score = 0
        row = clone.get_tiles()[rowNum]

        for x in row:
            if x == 0:
                if lastEmpty:
                    score -= 1
                else:
                    score -= 2
                lastEmpty = True
            else:
                score += 5
                lastEmpty = False

        # print("Row Score: ")
        # print(score)
        return score

    def getLandedScore(self, clone):
        score = clone.get_score()
        while clone.update() != True:
            None
            # print("update!")

        # print("Landed Score:")
        newScore = clone.get_score()
        bouns = 0
        # print(clone.get_tiles()[current])
        # print(newScore)
        if newScore - score > 100:
            bouns = 10
        # print(bouns)
        return bouns

    def getUpperRowHoleScore(self, clone):
        tiles = clone.get_tiles()
        score = 0
        for x in range(len(clone.get_tiles()[current])):
            if tiles[current - 1][x] != 0 and tiles[current][x] == 0:
                # 1
                # 0
                # _
                score -= 1
            if tiles[current - 2][x] != 0 and tiles[current - 1][x] != 0 and tiles[current][x] == 0:
                # 1
                # 0
                # 0
                # _
                score -= 1
        return score

    def getPredictedScore(self, clone):
        global current
        # print("------")
        # print(self.getRowScore(clone,current)  + self.getLandedScore(clone) )
        scoreLanded = self.getLandedScore(clone) * 10
        scoreRow = self.getRowScore(clone, current)
        # scoreHoles = self.getUpperRowHoleScore(clone) * 10

        return scoreLanded + scoreRow  # + scoreHoles

    def checkAllRotation(self, gamestate, posision):
        # global numToRotate
        maxMark = -100
        rotate = 0

        # print("check rotation")
        for i in range(0, 4):
            clone = gamestate.clone(True)
            # print("rotate!!")
            # print(i)
            for x in range(i):
                clone.rotate(Direction.RIGHT)
                clone.update()

            # print("called")
            for x in range(10):
                self.toPosition(clone, self.get_pos_to_move(clone, posision))
                clone.update()
            # print("ended")
            # clone.print_block_tiles()
            cScore = self.getPredictedScore(clone)
            if cScore > maxMark:
                maxMark = cScore
                rotate = i
            # clone = gamestate.clone(False)

        return maxMark, rotate

    def checkAllMoves(self, gamestate):
        global current, newGame
        maxMark = -100
        rotate = 0
        bestPos = 0
        count = 0
        possible = True

        for i in range(0, 10):

            # print("check position:")
            # print(i)
            cScore, cRotate = self.checkAllRotation(gamestate, i)
            if cScore == maxMark:
                count += 1
            if cScore > maxMark:
                maxMark = cScore
                rotate = cRotate
                bestPos = i

        # print("maxSore")
        # print(maxMark)
        #
        # print(bestPos)


        if bestPos == 0 and count >= 9 and newGame == False:
            print("NOT POSSIBLE!!!")
            current = current - 1
            possible = False
            if current < 19 - self.get_line_hight(gamestate):
                bestPos = random.random(0, 9)
                possible = True


        return bestPos, rotate, possible

    def get_line_hight(self,gamestate):
        return len(gamestate.get_tiles())

    def call_next(self, gamestate):
        global current, numToRotate, inProgress, posToMoveTo, newGame

        if gamestate.get_falling_block_position()[1] == 1:
            print("new block")
            current = current + 3
            if current > 19:
                current = 19
            possible = False
            while possible == False:
                posToMoveTo, numToRotate, possible = self.checkAllMoves(gamestate)
                print("possible")
                print(current)
            newGame = False

        # self.toPosition

        posToMove = self.get_pos_to_move(gamestate, posToMoveTo)

        if numToRotate > 0:
            # print("rotate?")
            # print(numToRotate)
            gamestate.rotate(Direction.RIGHT)
            numToRotate -= 1
            return

        # print("lme?")
        # print(posToMoveTo)
        # print("pos?")
        # print(posToMove)

        # gamestate.print_block_tiles()
        # self.getBlockWidth(gamestate)

        self.toPosition(gamestate, posToMove)

        # if(self.checkAllRotation(gamestate,posToMove,posToMoveTo) != -1):
        #     gamestate.rotate(Direction.RIGHT)
        #     numToRotate -= 1
        # else:
        #     print("!!!!!NOT POSSIBLE")
        #     if leftMostEmpty < 9:
        #         posToSkip = leftMostEmpty
        #     else:
        #         posToSkip = 0
        #         current -= 1

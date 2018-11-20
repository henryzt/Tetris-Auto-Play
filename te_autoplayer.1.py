''' Implement an AI to play tetris '''
from random import Random
from te_settings import Direction
import random


current = 19
numToRotate = 0
posToSkip = 0

class AutoPlayer():


    ''' A very simple dumb AutoPlayer controller '''
    def __init__(self, controller):
        global numToRotate, posToSkip, current
        self.controller = controller
        self.rand = Random()
        current = 19
        numToRotate = 0
        posToSkip = 0
      

    def next_move(self, gamestate):
        ''' next_move() is called by the game, once per move.
            gamestate supplies access to all the state needed to autoplay the game.'''
        self.random_next_move(gamestate)


    def toPosition(self, gamestate, position):
        
        if (position < gamestate.get_falling_block_position()[0]):
            gamestate.move(Direction.LEFT)
        elif (position > gamestate.get_falling_block_position()[0]):
            gamestate.move(Direction.RIGHT)
       


    def getNext(self, gamestate, list, value):
        i = 0
        for x in list:
            if x == value:
                return i                      
            i += 1
        return i

    def getNextSkip(self, gamestate, list, value,skip):
        i = 0
        for x in list:
            if x == value and i > skip:
                return i                      
            i += 1
        return i

    def getBlockBottomStart(self,gamestate):
        listLen = len(gamestate.get_falling_block_tiles())
        i = 1
        lastEmpty = -1
        for x in gamestate.get_falling_block_tiles():
            if self.getNext(gamestate,x,1) == listLen:
                lastEmpty = i
            i += 1

        if lastEmpty == -1:
            return gamestate.get_falling_block_tiles()[listLen - 1]
        return gamestate.get_falling_block_tiles()[lastEmpty - 2]

    def getBlockWidth(self,gamestate):
        pos = 0
        for x in gamestate.get_falling_block_tiles():
            count = 0
            for i in x:
                if i == 1:
                    if count > pos:
                        pos = count #update largest block exist
                count +=1
        return pos



    def checkLandedPossible(self, gamestate,posToMove,posision,clone):
        if posToMove == gamestate.get_falling_block_position()[0]:
            while clone.update() != True:
                None
                # print("update")
            print(clone.get_tiles()[current])
        else:
            return True
        # gamestate.print_tiles()
        print(clone.get_tiles()[current][posision])
        if clone.get_tiles()[current][posision] == 0 and self.getNext(gamestate,clone.get_tiles()[current],0) != -1:
            print("Block won't land to bottom")
            gamestate.clone(False)
            return False
        return True

    def checkAllRotation(self, gamestate, posToMove, posision):
        global numToRotate
        betterOne = -1
        clone = gamestate.clone(True)
        for i in range(4):
            print(clone.print_block_tiles())
            if self.checkLandedPossible(gamestate,posToMove,posision,clone):
                numToRotate = i
                if self.checkLandedPossible(gamestate,posToMove,posision + 1,clone):
                    betterOne = i
                elif self.checkLandedPossible(gamestate,posToMove,posision - 1,clone):
                    betterOne = i
            clone.rotate(Direction.RIGHT)
            self.toPosition(clone, posToMove)
            self.toPosition(clone, posToMove)
            self.toPosition(clone, posToMove)
            clone.update()
                
        if betterOne != -1:
            numToRotate = betterOne

        return numToRotate

    def random_next_move(self, gamestate):
        global current,numToRotate,posToSkip

        # print(gamestate.print_block_tiles())
        # print(gamestate.get_tiles()[current])

        blockBottomStart = self.getNext(gamestate, self.getBlockBottomStart(gamestate), 1)
        if blockBottomStart == len(gamestate.get_falling_block_tiles()):
            blockBottomStart = 0
        
        if posToSkip > 0:
            leftMostEmpty = self.getNextSkip(gamestate,gamestate.get_tiles()[current],0, posToSkip)
        else:
            leftMostEmpty = self.getNext(gamestate,gamestate.get_tiles()[current],0)

        posToMove = leftMostEmpty - blockBottomStart
        print("bigger?")
        print(leftMostEmpty + self.getBlockWidth(gamestate))
        if leftMostEmpty + self.getBlockWidth(gamestate) > 9:
            print("Bigger case!!!")
            posToMove = leftMostEmpty -( leftMostEmpty + self.getBlockWidth(gamestate) - 9)

        if numToRotate > 0:
            print("rotate?")
            print(numToRotate)
            gamestate.rotate(Direction.RIGHT)
            numToRotate -=1
            return

        print("lme?")
        print(leftMostEmpty)
        print("pos?")
        print(posToMove)

        gamestate.print_block_tiles()
        self.getBlockWidth(gamestate)

        if(self.checkLandedPossible(gamestate,posToMove,leftMostEmpty,gamestate.clone(True))): #self.checkPossible(gamestate,leftMostEmpty) and 
            self.toPosition(gamestate, posToMove)
            numToRotate = 0
        else:
            print("Can't land")
            if(self.checkAllRotation(gamestate,posToMove,leftMostEmpty) != -1):
                gamestate.rotate(Direction.RIGHT)
                numToRotate -= 1
            else:
                print("!!!!!NOT POSSIBLE")
                if leftMostEmpty < 9:
                    posToSkip = leftMostEmpty
                else:
                    posToSkip = 0
                    current -= 1

                





    



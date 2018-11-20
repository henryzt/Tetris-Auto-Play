''' Implement an AI to play tetris '''
from random import Random
from te_settings import Direction
import random


current = 19


class AutoPlayer():


    ''' A very simple dumb AutoPlayer controller '''
    def __init__(self, controller):
        global lastXPos, lastYPos, current
        self.controller = controller
        self.rand = Random()

      

    def next_move(self, gamestate):
        ''' next_move() is called by the game, once per move.
            gamestate supplies access to all the state needed to autoplay the game.'''
        self.random_next_move(gamestate)


    def toPosition(self, gamestate, position):
        global lastXPos, lastYPos
        
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

    def getBlockBottom(self,gamestate):
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

    def checkPossible(self, gamestate, position):
        global current
        possible = True
        for i in range(10):
            # print(gamestate.get_tiles()[current - i])
            # print(gamestate.get_tiles()[current - i][position])
            print(position)
            if(gamestate.get_tiles()[current - i][position] != 0):
                possible = False
        
        


        return possible

    def random_next_move(self, gamestate):
        global current

        print(gamestate.print_block_tiles())
        print(gamestate.get_tiles()[current])

        blockBottom = self.getNext(gamestate, self.getBlockBottom(gamestate), 1)
        if blockBottom == len(gamestate.get_falling_block_tiles()):
            blockBottom = 0
        leftMostEmpty = self.getNext(gamestate,gamestate.get_tiles()[19],0)
        posToMove = leftMostEmpty - blockBottom
        print(self.checkPossible(gamestate,leftMostEmpty))
        if(self.checkPossible(gamestate,leftMostEmpty)):
            self.toPosition(gamestate, posToMove)
        else:
            gamestate.rotate(Direction.RIGHT)





    



''' Implement an AI to play tetris '''
from random import Random
from te_settings import Direction
import random

last = Direction.LEFT
lastYPos = -1
current = 0
posToMove = 0
movedTo10 = False #for I type

class AutoPlayer():


    ''' A very simple dumb AutoPlayer controller '''
    def __init__(self, controller):
        global lastXPos, lastYPos, current
        self.controller = controller
        self.rand = Random()
        last = None
        lastXPos = -1
        lastYPos = 10
        current = 0
        posToMove = 0

      

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
        # else:
            # if lastTile != gamestate.get_falling_block_tiles():
                
                            
            

    def random_next_move(self, gamestate):
        global lastYPos,current, posToMove,movedTo10
        pos = [-1,1,3,5]

        
        if gamestate.get_falling_block_position()[1] == 1 : #new block
            gamestate.rotate(Direction.RIGHT)
            if(gamestate.get_falling_block_type()== "I"):
                print(movedTo10)
                if movedTo10:
                    posToMove = 9
                    movedTo10 = False
                else:
                    posToMove = 10
                    movedTo10 = True
                
            else:
                posToMove = pos [current]
                current = current + 1
                if current == 4:
                    current = 0
        self.toPosition(gamestate, posToMove)
        print(gamestate.get_falling_block_position()[0])
        


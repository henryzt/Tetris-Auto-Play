''' Implement an AI to play tetris '''
from random import Random
from te_settings import Direction

last = Direction.LEFT
lastXPos = -1

class AutoPlayer():


    ''' A very simple dumb AutoPlayer controller '''
    def __init__(self, controller):
        global lastXPos, last
        self.controller = controller
        self.rand = Random()
        last = Direction.LEFT
        lastXPos = -1
      

    def next_move(self, gamestate):
        ''' next_move() is called by the game, once per move.
            gamestate supplies access to all the state needed to autoplay the game.'''
        self.random_next_move(gamestate)


    def toOneDirection(self, direction, gamestate):
        global lastXPos, last
        print(lastXPos)
        if lastXPos != gamestate.get_falling_block_position()[0]:
            lastXPos = gamestate.get_falling_block_position()[0]
            gamestate.move(direction)
        else:
            print(last)
            if last == Direction.LEFT :
                last = Direction.RIGHT
            else:
                last = Direction.LEFT 
            

    def random_next_move(self, gamestate):
        global last
        if last == Direction.LEFT :
            self.toOneDirection(Direction.LEFT,gamestate)
        else:
            self.toOneDirection(Direction.RIGHT,gamestate)

''' Implement an AI to play tetris '''
from random import Random
from te_settings import Direction

class AutoPlayer():
    ''' A very simple dumb AutoPlayer controller '''
    def __init__(self, controller):
        self.controller = controller
        self.rand = Random()

    def next_move(self, gamestate):
        ''' next_move() is called by the game, once per move.
            gamestate supplies access to all the state needed to autoplay the game.'''
      #  self.random_next_move(gamestate)
        (maxrotation, maxposition, bump) = self.estimate(gamestate)
        self.realmove(maxrotation, maxposition, gamestate)
       # print(self.gethole(gamestate))
       # print(height)

    def random_next_move(self, gamestate):
        ''' make a random move and a random rotation.  Not the best strategy! '''
        rnd = self.rand.randint(-1, 1)
        if rnd == -1:
            direction = Direction.LEFT
        elif rnd == 1:
            direction = Direction.RIGHT
        if rnd != 0:
            gamestate.move(direction)
        rnd = self.rand.randint(-1, 1)
        if rnd == -1:
            direction = Direction.LEFT
        elif rnd == 1:
            direction = Direction.RIGHT
        if rnd != 0:
            gamestate.rotate(direction)
        gamestate.print_block_tiles()

    def estimate(self, gamestate):
        maxgrade = -9999
        score = 0
        maxscore = 0
        minhole = 200
        maxposition = 0
        maxrotation = 0
        for rotation in range(0, 4):
            for position in range(-2, 10):
                cloned_gamestate = gamestate.clone(True)
                grade = 0
                oldscore = cloned_gamestate.get_score()
                oldheight = self.getheight(cloned_gamestate)
                while True:
                    if cloned_gamestate.get_falling_block_angle() < rotation:
                        cloned_gamestate.rotate(Direction.RIGHT)
                    if cloned_gamestate.get_falling_block_position()[0] > position:
                        cloned_gamestate.move(Direction.LEFT)
                    elif cloned_gamestate.get_falling_block_position()[0] < position:
                        cloned_gamestate.move(Direction.RIGHT)
                    if cloned_gamestate.update():
                        break
                verhole = self.getverticalhole(cloned_gamestate)
                parhole = self.getparallelhole(cloned_gamestate)
                holenum = self.getholenum(cloned_gamestate)
                score = cloned_gamestate.get_score()
                height = self.getheight(cloned_gamestate)
                blockade = self.getblockade(cloned_gamestate)
                bump = self.getbump(cloned_gamestate)
                heightmedium = self.getheightmedium(cloned_gamestate)
            #    grade -= holenum * 8
                grade += ((score - oldscore) % 100) * 5
                grade -= verhole * 12
                grade -= parhole * 5
                grade += ((score - oldscore) // 100) * ((score - oldscore) // 100) * 5
            #    grade -= (height - oldheight) * 5
            #    grade -= bump * 4
            #    grade -= blockade * 3
            #    grade -= heightmedium * 5
                if grade > maxgrade:
                    maxgrade = grade
                    maxposition = position
                    maxrotation = rotation
        return(maxrotation, maxposition, height)

    def realmove(self, maxrotation, maxposition, gamestate):
    #    print("------", maxrotation, maxposition)
        if gamestate.get_falling_block_position()[0] > maxposition:
            gamestate.move(Direction.LEFT)
        elif gamestate.get_falling_block_position()[0] < maxposition:
            gamestate.move(Direction.RIGHT)
        if gamestate.get_falling_block_angle() < maxrotation:
            gamestate.rotate(Direction.RIGHT)
    
    def getspace(self, gamestate):
        space = 0
        settled_tiles = gamestate.get_tiles()
        for row in range(19, -1, -1):
            for col in range(0, 10):
                is_tiles = False
                if settled_tiles[row][col] == 0:
                    space += 1
                else:
                    is_tiles = True
            if not is_tiles:
                space -= 10
                break
        return(space)

    def getverticalhole(self, gamestate):
        hole = 0
        settled_tiles = gamestate.get_tiles()
        for col in range(0, 10):
            is_hole = False
            for row in range(19, -1, -1):
                if settled_tiles[row][col] == 0:
                    is_hole = True
                else:
                    if is_hole == True:
                        is_hole = False
                        hole += 1
      #  print(hole)
        return(hole)

    def getholenum(self, gamestate):
        holenum = 0
        temp_holenum = 0
        settled_tiles = gamestate.get_tiles()
        for col in range(0, 10):
            is_hole = False
            temp_holenum = 0
            for row in range(19, -1, -1):
                if settled_tiles[row][col] == 0:
                    is_hole = True
                    temp_holenum += 1
                else:
                    if is_hole == True:
                        is_hole = False
                        holenum += temp_holenum
                        temp_holenum = 0
      #  print(hole)
        return(holenum)    
    
    def getheight(self, gamestate):
        settled_tiles = gamestate.get_tiles()
        height = 0
        for col in range(0, 10):
            for row in range(0, 20):
                if settled_tiles[row][col] != 0:
                    height += (20 - row)
                    break
        return(height)

    def getblockade(self, gamestate):
        blockade = 0
        settled_tiles = gamestate.get_tiles()
        for col in range(0, 10):
            is_hole = False
            for row in range(19, -1, -1):
                if settled_tiles[row][col] == 0:
                    is_hole = True
                else:
                    if is_hole == True:
                        blockade += 1
        return(blockade)

    def getbump(self, gamestate):
        settled_tiles = gamestate.get_tiles()
        prev_height = 0
        height = 0
        bump = 0
        for row in range(0, 20):
            if settled_tiles[row][0] != 0:
                bump -= (20 - row)
                break
        for col in range(0, 10):
            for row in range(0, 20):
                if settled_tiles[row][col] != 0:
                    prev_height = height
                    height = (20 - row)
                    bump += abs(height - prev_height)
                    break      
        return(bump)  

    def getheightmedium(self, gamestate):
        settled_tiles = gamestate.get_tiles()
        maxheight = 0
        minheight = 999
        height = 0
        for col in range(0, 10):
            for row in range(0, 20):
                if row == 19:
                    if settled_tiles[row][col] != 0:
                        height = (20 - row)
                    else:
                        height = 0
                    if height > maxheight:
                        maxheight = height
                    if height <= minheight:
                        minheight = height
                    break
                if settled_tiles[row][col] != 0:
                    height = (20 - row)
                    if height > maxheight:
                        maxheight = height
                    if height <= minheight:
                        minheight = height
                    break
        return((maxheight - minheight) / 2)

    def getparallelhole(self, gamestate):
        hole = 0
        settled_tiles = gamestate.get_tiles()
        for row in range(19, -1, -1):
            is_hole = False
            for col in range(0, 10):
                if settled_tiles[row][col] == 0:
                    is_hole = True
                else:
                    if is_hole == True:
                        is_hole = False
                        hole += 1
      #  print(hole)
        return(hole)


        

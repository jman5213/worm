




import random, pygame, sys
from pygame.locals import*

FPS = 15
WINDOWWIDTH = 640
WINDOWHIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHIGHT % CELLSIZE == 0, "Window width must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHIGHT = int(WINDOWHIGHT / CELLSIZE) 

#             r   g   b
WHITE     = (225,225,225)
BLACK     = (  0,  0,  0)
RED       = (225,  0,  0)
GREEN     = (  0,225,  0)
DARKGREEN = (  0,155,  0)
DARKGREY  = ( 40, 40, 40)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head

def main():
  global FPSLOCK, DISPLAYSURF, BASICFONT

  pygame.init()
  FPSLOCK = pygame.time.Clock()
  DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHIGHT))
  BASICFONT = pygame.font.Font('freesansbold.tff', 18)
  pygame.display.set_caption('Wormy')

  showStartScreen()
  while True:
    runGame()
    showGameOverScreen()

def runGame():
  # Set a random start point.
  startx = random.randint(5, CELLWIDTH - 6)
  starty = random.randint(5, CELLHIGHT - 6)
  wormCords = [{'x':startx,     'y':starty},
               {'x':startx - 1, 'y':starty},
               {'x':startx - 2, 'y':starty}]
  direction = RIGHT

  # Start apple in a random place.
  apple = getRandomLocation()

  while True:
    for event in pygame.event.get():# event handeling loop
      if event.type == QUIT:
        terminate()
      elif event.type == KEYDOWN:
        if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
          direction = LEFT
        elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
          direction = RIGHT
        elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
          direction = DOWN
        elif event.key == K_ESCAPE:
          terminate()

    # check if th worm has hit itself or edge
    if wormCords[HEAD]['x'] == -1 or wormCords[HEAD]['x'] == CELLWIDTH or wormCords[HEAD]['y'] == -1 or wormCords[HEAD]['y'] == CELLHIGHT:
      return# game over 
    for wormBody in wormCords[1:]:
      if wormBody['x'] == wormCords[HEAD]['x'] and wormBody['y'] == wormCords[HEAD]['y'] == CELLHIGHT:         
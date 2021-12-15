




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
        return#game over
      for wormBody in wormCords[1:]:
        if wormBody['x'] == wormCords[HEAD]['x'] and wormBody['y'] == wormCords[HEAD]['y']:
          return#game over 
    #check if worm has eaten an apple
    if wormCords[HEAD]['x'] == apple['x'] and wormCords[HEAD]['y'] == apple['y']:
      #don't remove worm's tail segment
      apple = getRandomLocation()#makes new apple
    else:
      del wormCords[-1]#remove worm's tail segment

    #move the worm by adding a segment in the direction it is moving
    if direction == UP:
      newHead = {'x': wormCoords[HEAD]['x'], 'y':wormCoords[HEAD]['y'] - 1}
    elif direction == DOWN:
      newHead = {'x': wormCoords[HEAD]['x'], 'y':wormCoords[HEAD]['y'] + 1}
    elif direction == LEFT:
      newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y':wormCoords[HEAD]['y']}
    elif direction == RIGHT:
      newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y':wormCoords[HEAD]['y']}
    wormCords.insert(0, newHead)
    DISPLAYSURF.fill(BGCOLOR)
    drawgrid()
    drawWorm(wormCords)
    drawApple(apple)
    drawScore(len(wormCords)- 3)
    pygame.display.update()
    FPSLOCK.tick(FPS)

def showStartScreen():
  titleFont = pygame.font.Font('freesansbold.ttf', 100)
  titleSurf1 = titleFont.render('Wormy!', True, WHITE, DARKGREEN)
  titleSurf2 = titleFont.render('Wormy!', True, GREEN)

  degrees1 = 0
  degrees2 = 0
  while True:
    DISPLAYSURF.fill(BGCOLOR)
    rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
    rotatedRect1 = rotatedSurf1.get_rect()
    rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
    DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

    rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
    rotatedRect2 = rotatedSurf2.get_rect()
    rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
    DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

    drawPressKeyMsg()

    if checkForKeyPress():
      pygame.event.get()#clear event queue
      return
    pygame.display.update()
    FPSLOCK.tick(FPS)
    degrees1 += 3#rotate by 3 degrees each frame
    degrees2 += 7#rotate by 7 degrees each frame


def terminate():
  pygame.quit()
  sys.exit()


def getRandomLocation():
  return{'x':random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHIGHT - 1)}


def showGameOverScreen():
  gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
  gameSurf = gameOverFont.render('Game', True, WHITE)
  overSurf = gameOverFont.render('Over', True, WHITE)
  gameRect = gameSurf.get_rect()
  overRect = overSurf.get_rect()
  gameRect.midtop = (WINDOWWIDTH / 2, 10)
  overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

  DISPLAYSURF.blit(gameSurf, gameRect)
  DISPLAYSURF.blit(overSurf, overRect)
  drawPressKeyMsg()
#I AM AT THE TOP OF PAGE 136
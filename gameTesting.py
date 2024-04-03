import pygame, sys
import random
import neat
import math
import os

# Constants
WIDTH, HEIGHT = 1850, 990
TITLE = "Evolution sim"
# pygame initialization
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()


# Player Class
class Predator:
 def __init__(self, x, y, energy):
     self.energy = energy
     self.x = int(x)
     self.y = int(y)
     self.rect = pygame.Rect(self.x, self.y, 32, 32)
     self.color = (250, 120, 60)
     self.velX = 0
     self.velY = 0
     self.left_pressed = False
     self.right_pressed = False
     self.up_pressed = False
     self.down_pressed = False
     self.speed = 4
 def draw(self, win):
     pygame.draw.rect(win, self.color, self.rect)
 def addEnergy(self):
     self.energy+=0.499999999
 def update(self):
     self.velX = 0
     self.velY = 0
     if self.left_pressed and not self.right_pressed:
         self.velX = -self.speed
     if self.right_pressed and not self.left_pressed:
         self.velX = self.speed
     if self.up_pressed and not self.down_pressed:
         self.velY = -self.speed
     if self.down_pressed and not self.up_pressed:
         self.velY = self.speed
     self.x += self.velX
     self.y += self.velY
     self.energy -= 0.0333333333
     self.rect = pygame.Rect(int(self.x), int(self.y), 32, 32)
class Prey:
 def __init__(self, x, y,energy):
     self.x = int(x)
     self.y = int(y)
     self.rect = pygame.Rect(self.x, self.y, 32, 32)
     self.color = (0, 255, 0)
     self.energy=energy
     self.velX = 0
     self.velY = 0
     self.left_pressed = False
     self.right_pressed = False
     self.up_pressed = False
     self.down_pressed = False
     self.speed = 2
 def draw(self, win):
     pygame.draw.rect(win, self.color, self.rect)
 def addEnergy(self):
     self.energy+=0.499999999

 def update(self):
     self.velX = 0
     self.velY = 0
     if self.left_pressed and not self.right_pressed:
         self.velX = -self.speed
     if self.right_pressed and not self.left_pressed:
         self.velX = self.speed
     if self.up_pressed and not self.down_pressed:
         self.velY = -self.speed
     if self.down_pressed and not self.up_pressed:
         self.velY = self.speed
     self.x += self.velX
     self.y += self.velY
     self.energy-=0.0333333333
     self.rect = pygame.Rect(int(self.x), int(self.y), 32, 32)
# Player Initialization
predatorArray = []
preyArray = []

def preyMovement(prey, preyInputNum):
   prey_x, prey_y, closest_x, closest_y = preyInputNum
   distance = math.sqrt((prey_x - closest_x)**2 + (prey_y - closest_y)**2)
   if distance > 0:
       move_eval = (closest_x - prey_x) / distance, (closest_y - prey_y) / distance
       if move_eval[0] > 0:
           prey.right_pressed = True
           prey.left_pressed = False
       else:
           prey.left_pressed = True
           prey.right_pressed = False

       if move_eval[1] > 0:
           prey.down_pressed = True
           prey.up_pressed = False
       else:
           prey.up_pressed = True
           prey.down_pressed = False
   else:
       prey.right_pressed = False
       prey.left_pressed = False
       prey.up_pressed = False
       prey.down_pressed = False
   prey.update()

def endgame():
 exit()

class Pellets:
 def __init__(self, x,y):
     self.x = int(x)
     self.y = int(y)
     self.rect = pygame.Rect(self.x, self.y, 10, 10)
     self.color = (255, 255, 255)
 def draw(self, win):
     pygame.draw.rect(win, self.color, self.rect)


def drawPellets(win, pelletArray):
 for pa in pelletArray:
     pa.draw(win)
def isEat(prey, pelletArray):
 for pa in pelletArray:
     if (prey.rect.colliderect(pa)):
         prey.addEnergy()
         pelletArray.remove(pa)
 # return pelletArray
 #prey.isTouchingBorder()
class River:
 def __init__(self, x, y):
     self.x = int(x)
     self.y = int(y)
     self.rect = pygame.Rect(self.x, self.y, 250, 200)
     self.color = (100, 100, 100)
 def draw(self, win):
     pygame.draw.ellipse(win, (0,0,255),self.rect)
def drawBoundary(screen):
  for pr in preyArray:
      print("y " + str(pr.y))
      print("x " + str(pr.x))
      if (pr.y <= 3):
          while (pr.y <= 3):
              pr.y += 10
      if (pr.x <= 1):
          while (pr.x <= 1):
              pr.x += 10
      if (pr.x >= 1817):
          while (pr.x >= 1817):
              pr.x -= 10
      if (pr.y >= 955):
          while (pr.y >= 955):
              pr.y -= 10
  for pr in predatorArray:
      if (pr.y <= 3):
          while (pr.y <= 3):
              pr.y += 10
      if (pr.x <= 1):
          while (pr.x <= 1):
              pr.x += 10
      if (pr.x >= 1817):
          while (pr.x >= 1817):
              pr.x -= 10
      if (pr.y >= 955):
          while (pr.y >= 955):
              pr.y -= 10

def isDead(prey):
  if prey.energy <= 0:
      return 1
  else:
      return 2

def getPreyInput(prey, pelletArray):
  closest_X = 0
  closest_Y = 0
  prey_X = prey.x
  prey_Y = prey.y
  closest_Distance = 1000000
  for i in pelletArray:
      if abs(math.hypot(prey_X-i.x, prey_Y-i.y)) < abs(closest_Distance):
          closest_Distance = abs(math.hypot(prey_X-i.x, prey_Y-i.y))
          closest_X = i.x
          closest_Y = i.y
  pygame.draw.aaline(win, (255, 255, 255), (prey_X, prey_Y), (closest_X, closest_Y))
  return [prey.x-closest_X, prey.y- closest_Y]

def eval_genome(preygenomes, config):
  river = River(random.randint(0, WIDTH), random.randint(0, HEIGHT))
  pelletArray = []
  for i in range(50):
      pellets = Pellets(random.randint(0, WIDTH), random.randint(0, HEIGHT))
      pelletArray.append(pellets)
  preyArray = []
  preyNets = []
  preyGe = []
  for genome_id, genome in preygenomes:
      genome.fitness = 0
      net = neat.nn.FeedForwardNetwork.create(genome, config)
      preyNets.append(net)
      preyArray.append(Prey((WIDTH / 2) + 100, (HEIGHT / 2) + 100, 100))
      preyGe.append(genome)
  run = True
  while run and len(preyArray) > 0:
     for event in pygame.event.get():
         if event.type == pygame.QUIT:
             run = False
             pygame.quit()
             sys.exit()
     win.fill((12, 24, 36))
     river.draw(win)
     i = 0
     x = len(preyArray)
     while i < x:
         preyArray[i].draw(win)
         preyArray[i].update()
         preyGe[i].fitness += 0.1
         prey_output = preyNets[i].activate(getPreyInput(preyArray[i], pelletArray))
         #print("parr " + str(int(i)) + " outs " + str(prey_output))
         # maxVal = 0
         # indexOfMax = 0
         # minVal = 400
         # indexOfMin = 0
         # for zn in range(len(prey_output)):
         #       if (prey_output[zn]>maxVal):
         #           maxVal=prey_output[zn]
         #           indexOfMax=zn
         #       if (prey_output[zn]<minVal):
         #           minval = prey_output[zn]
         #           indexOfMin=[zn]
         preyMovement(preyArray[i], prey_output)
         # preyMovement(preyArray[i], minVal)
         # preyMovement(preyArray[i], (abs(minVal)*-1))
         # preyMovement(preyArray[i], (abs(maxVal)*-1))
         # pelletArray = isEat(preyArray[i],pelletArray)
         isEat(preyArray[i], pelletArray)
         if isDead(preyArray[i]) == 1:
             preyNets.pop(i)
             preyGe.pop(i)
             preyArray.pop(i)
             x-=1
         i += 1
     drawPellets(win, pelletArray)
     drawBoundary(win)
     pygame.display.flip()
     clock.tick(120)
def run(config_file):
  config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                       neat.DefaultSpeciesSet, neat.DefaultStagnation,
                       config_file)
  p = neat.Population(config)
  p.add_reporter(neat.StdOutReporter(True))
  stats = neat.StatisticsReporter()
  p.add_reporter(stats)
  # Run for up to 50 generations.
  winner = p.run(eval_genome, 50)
  # show final stats
  print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
  # Determine path to configuration file. This path manipulation is
  # here so that the script will run successfully regardless of the
  # current working directory.
  local_dir = os.path.dirname(__file__)
  config_path = os.path.join(local_dir, 'config.txt')
  run(config_path)


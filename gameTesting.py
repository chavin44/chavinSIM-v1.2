import pygame, sys
import random
import neat
import math
import os
from tkinter import *
from tkinter import ttk

root = Tk()
height = root.winfo_screenheight()

width = root.winfo_screenwidth()
print(str(height) + " " + str(width))
# Constants
# WIDTH, HEIGHT = 1850, 990
TITLE = "Evolution sim"
# pygame initialization
pygame.init()
win = pygame.display.set_mode((width - 100, height - 100))
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
        self.energy += 0.499999999

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
    def __init__(self, x, y, energy):
        self.x = int(x)
        self.y = int(y)
        self.rect = pygame.Rect(self.x, self.y, 32, 32)
        self.color = (0, 255, 0)
        self.energy = energy
        self.velX = 0
        self.velY = 0
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 4

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect,border_radius=2)

    def addEnergy(self):
        self.energy += 0.499999999

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

predatorArray = []
preyArray = []

def preyMovement(prey, preyInputNum):
    prey_x, prey_y, closest_x, closest_y = preyInputNum
    distance = math.sqrt((prey_x - closest_x) ** 2 + (prey_y - closest_y) ** 2)
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
    def __init__(self, x, y):
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
    # prey.isTouchingBorder()
class EnergyBar:
    def __init__(self, x, y, energy, color):
        self.energy = energy
        self.x = int(x)
        self.y = int(y)
        self.width = 100
        self.height = 10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = color

    def draw(self, win):
        current_width = int(self.width * (self.energy / 100))
        adjusted_rect = pygame.Rect(self.x, self.y, current_width, self.height)
        red = int(255 * (1 - self.energy / 100))
        green = int(128 * (self.energy / 100))
        blue = 0
        color = (red, green, blue)
        pygame.draw.rect(win, color, adjusted_rect, border_radius=4)

class River:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.rect = pygame.Rect(self.x, self.y, 250, 200)
        self.color = (100, 100, 100)

    def draw(self, win):
        pygame.draw.ellipse(win, (0, 0, 255), self.rect)


def drawBoundary(pr, screen):
    if (pr.y <= -10):
        while (pr.y <= -10):
            pr.y += 10
    if (pr.x <= -10):
        while (pr.x <= -10):
            pr.x += 10
    if (pr.x >= width - 110):
        while (pr.x >= width - 110):
            pr.x -= 10
    if (pr.y >= height - 110):
        while (pr.y >= height - 110):
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
        if abs(math.hypot(prey_X - i.x, prey_Y - i.y)) < abs(closest_Distance):
            closest_Distance = abs(math.hypot(prey_X - i.x, prey_Y - i.y))
            closest_X = i.x
            closest_Y = i.y
    pygame.draw.aaline(win, (255, 255, 255), (prey_X, prey_Y), (closest_X, closest_Y))
    return [prey.x - closest_X, prey.y - closest_Y]
class PreyID:
    def __init__(self, prey, IDNum):
        self.width = 100
        self.height = 10
        self.x = prey.x-25
        self.y = prey.y+25
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = (0, 0, 0)
        self.IDNum = IDNum
        self.font = pygame.font.Font(None, 24)

    def draw(self, win):
        text = self.font.render(str(self.IDNum), True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.midtop = (self.x + self.width // 2, self.y - text_rect.height)
        win.blit(text, text_rect)
def eval_genome(preygenomes, config):
    river = River(random.randint(100, width - 100), random.randint(100, height - 100))
    pelletArray = []
    for i in range(50):
        pellets = Pellets(random.randint(100, width - 100), random.randint(100, height - 100))
        pelletArray.append(pellets)
    preyArray = []
    preyNets = []
    preyGe = []
    for genome_id, genome in preygenomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        preyNets.append(net)
        preyArray.append(Prey((width / 2) + 100, (height / 2) + 100, 100))
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
            preyMovement(preyArray[i], prey_output)
            drawBoundary(preyArray[i], win)
            isEat(preyArray[i], pelletArray)
            # isRiver(preyArray[i], river)
            energyBar = EnergyBar(preyArray[i].x-25, preyArray[i].y-20, preyArray[i].energy, (max(0,preyArray[i].energy), 137, 100))
            energyBar.draw(win)
            if isDead(preyArray[i]) == 1:
                preyNets.pop(i)
                preyGe.pop(i)
                preyArray.pop(i)
                x -= 1
            i += 1
        drawPellets(win, pelletArray)
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

# no stealing im watching you....
import pygame, sys
import math
import random
import neat

WIDTH, HEIGHT = 1850, 990
TITLE = "CS Club Project | EvoSim"
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()


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

    #
    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect, border_radius=4)

    def addEnergy(self):
        self.energy += 12.499999999

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

    def removeEnergy(self):
        self.energy-= 7 + (1/3)


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
        pygame.draw.rect(win, self.color, self.rect, border_radius=4)

    def addEnergy(self):
        self.energy += 5.499999999

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
    def removeMeatEnergy(self):
        self.energy-= 7 + (1/3)
    def removeEnergy(self):
        self.energy-=100


# class PreyChild:
#     def __init__(self,x,y,energy,neuralNet):


predatorArray = []
preyArray = []
preyChildArray = []
predatorChildArray = []

predator = Predator((WIDTH / 2) + 100, (HEIGHT / 2) + 100, 100)
predatorArray.append(predator)
prey = Prey(WIDTH / 2 - 100, HEIGHT / 2 - 100, 100)
preyArray.append(prey)


def drawBoundary(screen):
    print("y " + str(prey.y))
    print("x " + str(prey.x))
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


def predatorMovement():
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            predator.left_pressed = True
        if event.key == pygame.K_RIGHT:
            predator.right_pressed = True
        if event.key == pygame.K_UP:
            predator.up_pressed = True
        if event.key == pygame.K_DOWN:
            predator.down_pressed = True
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT:
            predator.left_pressed = False
        if event.key == pygame.K_RIGHT:
            predator.right_pressed = False
        if event.key == pygame.K_UP:
            predator.up_pressed = False
        if event.key == pygame.K_DOWN:
            predator.down_pressed = False
def preyMovement():
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a:
            prey.left_pressed = True
        if event.key == pygame.K_d:
            prey.right_pressed = True
        if event.key == pygame.K_w:
            prey.up_pressed = True
        if event.key == pygame.K_s:
            prey.down_pressed = True
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_a:
            prey.left_pressed = False
        if event.key == pygame.K_d:
            prey.right_pressed = False
        if event.key == pygame.K_w:
            prey.up_pressed = False
        if event.key == pygame.K_s:
            prey.down_pressed = False

def endgame():
    exit()


def isKill():
    if (predator.rect.colliderect(prey)):
        predator.addEnergy()
        prey.removeEnergy()
class Meat:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        #self.vertices = [(self.x, self.y), (self.x+int(random.randint(0,5)), self.y++int(random.randint(0,10))), (self.x+int(random.randint(0,10)), self.y+int(random.randint(0,5))), (self.x+int(random.randint(0,15)), self.y+10), (self.x+20, self.y)]
        self.color = (139, 0, 0)  # Dark red
        self.rect = pygame.Rect(self.x, self.y, 10, 10)

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect, border_radius=100)


meatArray = []
for i in range(7):
    meat = Meat(random.randint(0, WIDTH), random.randint(0, HEIGHT))
    meatArray.append(meat)
def drawMeats(win):
    while (len(pelletArray) < 15):
        meat = Meat(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        meatArray.append(meat)
    for mt in meatArray:
        mt.draw(win)

class Pellets:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.rect = pygame.Rect(self.x, self.y, 10, 10)
        self.color = (153, 204, 255)

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect, border_radius=100)
pelletArray = []
for i in range(15):
    pellets = Pellets(random.randint(0, WIDTH), random.randint(0, HEIGHT))
    pelletArray.append(pellets)


def drawPellets(win):
    while (len(pelletArray) < 15):
        pellets = Pellets(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        pelletArray.append(pellets)
    for pa in pelletArray:
        pa.draw(win)

def predEatPell():
    for pa in pelletArray:
        if (predator.rect.colliderect(pa)):
            predator.removeEnergy()
            pelletArray.remove(pa)
def preyEatMeat():
    for mt in meatArray:
        if (prey.rect.colliderect(mt)):
            prey.removeMeatEnergy()
            meatArray.remove(mt)
def isEat():
    for pa in pelletArray:
        if (prey.rect.colliderect(pa)):
            prey.addEnergy()
            pelletArray.remove(pa)
    # prey.isTouchingBorder()


class River:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.rect = pygame.Rect(self.x, self.y, 250, 200)
        self.color = (100, 100, 100)

    def draw(self, win):
        pygame.draw.ellipse(win, (0, 0, 255), self.rect)
river = River(random.randint(0, WIDTH), random.randint(0, HEIGHT))

def dispNeuralNetPrey():
    pass


def dispNeuralNetPred():
    pass


class HealthBar:
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
        pygame.draw.rect(win, self.color, adjusted_rect, border_radius=4)


def dispHealthBarPrey():
    preyHPBAR = HealthBar(50, 100, prey.energy, (0, 137, 100))
    preyHPBAR.draw(win)


def dispHealthBarPred():
    predHPBAR = HealthBar(WIDTH - 250, 100, predator.energy, (140, 0, 0))
    predHPBAR.draw(win)


def checkIfDead():
    if (prey.energy <=0 or predator.energy<=0):
        endgame()
def isEatMeat():
    for pa in meatArray:
        if (predator.rect.colliderect(pa)):
            predator.addEnergy()
            meatArray.remove(pa)


def gamingtrus():
    isKill()
    win.fill((60, 60, 60))
    river.draw(win)
    predator.draw(win)
    prey.draw(win)
    # update
    predator.update()
    prey.update()
    # istb()
    drawPellets(win)
    drawMeats(win)
    isEat()
    isEatMeat()
    predEatPell()
    preyEatMeat()
    drawBoundary(win)
    checkIfDead()
    dispNeuralNetPrey()
    dispNeuralNetPred()
    dispHealthBarPrey()
    dispHealthBarPred()
    pygame.display.flip()
    print("Predator Energy: " + str(predator.energy))
    print("Prey Energy: " + str(prey.energy))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        predatorMovement()
        isKill()
        preyMovement()
        isKill()
    gamingtrus()
    clock.tick(120)

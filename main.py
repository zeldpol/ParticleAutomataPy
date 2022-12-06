import pygame as pg
import random
import math

pg.init()
screenWidth, screenHeight = 1280, 720
fps = 30
timer = pg.time.Clock()
screen = pg.display.set_mode([screenWidth, screenHeight])

MAX_DIST = 100
fw = math.floor(screenWidth / MAX_DIST) + 1
fh = math.floor(screenHeight / MAX_DIST) + 1

NODE_RADIUS = 5
NODE_COUNT = 1000
SPEED = 4
PLAYBACK_SPEED = 3
BORDER = 30

links = []
LINK_FORCE = -0.015
COUPLING = [
    [1, 1, -1],
    [1, 1, 1],
    [1, 1, 1]
]
LINKS = [1, 3, 2]
LINKS_POSSIBLE = [
    [0, 1, 1],
    [1, 2, 1],
    [1, 1, 2],
]
COLORS = [
    'rgb(250, 20, 20)',
    'rgb(200, 140, 100)',
    'rgb(80, 170, 140)',
]


class Particle:
    def __init__(self, type, x, y):
        self.type = type
        self.x = x
        self.y = y

    def fx(self):
        return math.floor(self.x / MAX_DIST)

    def fy(self):
        return math.floor(self.y / MAX_DIST)

a=2

class Field:
    particles = []

    def __init__(self, i, j):
        self.i = i
        self.j = .


fields = []
for i in range(fw):
    for j in range(fh):
        fields.append(Field(i, j))

for i in range(NODE_COUNT):
    type = random.randint(0, len(COUPLING))
    x = random.randint(0, screenWidth)
    y = random.randint(0, screenHeight)
    p = Particle(type, x, y)
    field = fields[p.fx()][p.fy()]
    field.particles.push(p)

BG = 'rgb(20, 55, 75)'
LINK = 'rgb(255, 230, 0)'

pg.draw.circle(screen, (55, 55, 55), (random.randint(0, 1000), random.randint(0, 600)), 5)
pg.draw.circle(screen, (55, 55, 55), (random.randint(0, 1000), random.randint(0, 600)), 5)
pg.draw.circle(screen, (55, 55, 55), (random.randint(0, 1000), random.randint(0, 600)), 5)

running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    timer.tick(fps)
    screen.fill(BG)
    pg.display.update()

pg.quit()

import pygame as pg
import random
import math

pg.init()
screenWidth, screenHeight = 1280, 720
fps = 2
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
    (250, 20, 20),
    (200, 140, 100),
    (80, 170, 140),
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


class Field:
    particles = []

    def __init__(self, i, j):
        self.i = i
        self.j = j


fields = []
for i in range(fw):
    fields.append([])
    for j in range(fh):
        fields[i].append(Field(i, j))

for i in range(NODE_COUNT):
    pointType = random.randint(0, len(COUPLING))
    x = random.randint(0, screenWidth)
    y = random.randint(0, screenHeight)
    p = Particle(pointType, x, y)
    field = fields[p.fx()][p.fy()]
    field.particles.append(p)

backgroundColor = (20, 55, 75)
LINK = (255, 230, 0)


def draw_scene():
    screen.fill((20, 55, 75))

    for p in field.particles:
        pg.draw.circle(screen, COLORS[p.type-1], (p.x, p.y), NODE_RADIUS)

    return 0


running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    timer.tick(fps)
    draw_scene()


    pg.display.flip()
pg.quit()

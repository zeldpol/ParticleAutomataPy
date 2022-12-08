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
    (250, 20, 20),
    (200, 140, 100),
    (80, 170, 140),
]


class Particle:
    def __init__(self, type, x, y):
        self.type = type
        self.x = x
        self.y = y
        self.sx = 0
        self.sy = 0
        self.links = 0
        self.bonds = []

    def fx(self):
        return math.floor(self.x / MAX_DIST)

    def fy(self):
        return math.floor(self.y / MAX_DIST)


class Field:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.particles = []


fields = []
for i in range(fw):
    column = []
    for j in range(fh):
        column.append(Field(i, j))
    fields.append(column)

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

    for col in fields:
        for field in col:
            for p in field.particles:
                pg.draw.circle(screen, COLORS[p.type - 1], (p.x, p.y), NODE_RADIUS)

    return 0


def logic():

    for col in fields:
        for field in col:
            for p in field.particles:
                p.x += p.sx
                p.y += p.sy
                p.sx *= 0.98
                p.sy *= 0.98
                magnitude = math.sqrt(p.sx ** 2 + p.sy ** 2)
                if magnitude > 1:
                    p.sx /= magnitude
                    p.sy /= magnitude

                if p.x < BORDER:
                    p.sx += SPEED * 0.05
                    if p.x < 0:
                        p.sx *= -0.5

                elif p.x > screenWidth - BORDER:
                    p.sx -= SPEED * 0.05
                    if p.x > screenWidth:
                        p.x = screenWidth * 2 - p.x
                        p.sx *= -0.5

                if p.y < BORDER:
                    p.sy += SPEED * 0.05
                    if p.y < 0:
                        p.y = -p.y
                        p.sy *= -0.5

                elif p.y > screenHeight - BORDER:
                    p.sy -= SPEED * 0.05
                    if p.y > screenHeight:
                        p.y = screenHeight * 2 - p.y
                        p.sy *= -0.5

    for link, a, b in links:
        d2 = (a.x - b.x) ** 2 + (a.y - b.y) ** 2
        if d2 > MAX_DIST ** 2 / 4:
            a.links -= 1
            b.links -= 1
            a.bonds.remove(b)
            b.bonds.remove(a)
            links.remove(link)

        elif d2 > NODE_RADIUS ** 2 * 4:
            angle = math.atan2(a.y-b.y, a.x - b.x)
            a.sx += math.cos(angle) * LINK_FORCE * SPEED
            a.sy += math.sin(angle) * LINK_FORCE * SPEED
            b.sx -= math.cos(angle) * LINK_FORCE * SPEED
            b.sy -= math.sin(angle) * LINK_FORCE * SPEED

    for col in fields:
        for f in col:
            for p in f.particles:
                if p.fx() == f.i and p.fy() == f.j:
                    continue
                print(f'({f.i},{f.j}) -> ({p.fx()},{p.fy()})')
                f.particles.remove(p)
                fields[p.fx()][p.fy()].particles.append(p)

running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    timer.tick(fps)
    draw_scene()
    logic()

    pg.display.flip()
pg.quit()

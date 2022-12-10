import pygame as pg
import random
import math

pg.init()
screenWidth, screenHeight = 1280, 720
fps = 60
timer = pg.time.Clock()
screen = pg.display.set_mode([screenWidth, screenHeight])

MAX_DIST = 100
fw = math.floor(screenWidth / MAX_DIST) + 1
fh = math.floor(screenHeight / MAX_DIST) + 1

NODE_RADIUS = 5
NODE_COUNT = 500
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


class Link:
    def __init__(self, a, b):
        self.a = a
        self.b = b


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


BG = (20, 55, 75)
LINK = (255, 230, 0)


def draw_scene():
    screen.fill(BG)

    for col in fields:
        for field in col:
            for p in field.particles:
                pg.draw.circle(screen, COLORS[p.type - 1], (p.x, p.y), NODE_RADIUS)

                for b in p.bonds:
                    pg.draw.line(screen, LINK, (p.x, p.y), (b.x, b.y))



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

    for link in links:
        a = link.a
        b = link.b
        d2 = (a.x - b.x) ** 2 + (a.y - b.y) ** 2
        if d2 < NODE_RADIUS:
            d2 = NODE_RADIUS
        if d2 > MAX_DIST ** 2 / 4:
            a.links -= 1
            b.links -= 1
            a.bonds.remove(b)
            b.bonds.remove(a)
            links.remove(link)

        elif d2 > NODE_RADIUS ** 2 * 4:
            angle = math.atan2(a.y - b.y, a.x - b.x)
            a.sx += math.cos(angle) * LINK_FORCE * SPEED
            a.sy += math.sin(angle) * LINK_FORCE * SPEED
            b.sx -= math.cos(angle) * LINK_FORCE * SPEED
            b.sy -= math.sin(angle) * LINK_FORCE * SPEED

    for col in fields:
        for f in col:
            for p in f.particles:
                if p.fx() == f.i and p.fy() == f.j:
                    continue
                f.particles.remove(p)
                fields[p.fx()][p.fy()].particles.append(p)

    # ChatGPT

    for col in fields:
        for f in col:
            for i1, a in enumerate(f.particles):
                for j1 in range(i1 + 1, len(f.particles)):
                    b = f.particles[j1]
                    apply_force(a, b)

            if f.i < fw - 1:
                field1 = fields[f.i + 1][f.j]
                for j1 in range(len(field1.particles)):
                    b = field1.particles[j1]
                    apply_force(a, b)

            if f.j < fh - 1:
                field1 = fields[f.i][f.j + 1]
                for j1 in range(len(field1.particles)):
                    b = field1.particles[j1]
                    apply_force(a, b)

            if f.i < fw - 1 and f.j < fh - 1:
                field1 = fields[f.i + 1][f.j + 1]
                for j1 in range(len(field1.particles)):
                    b = field1.particles[j1]
                    apply_force(a, b)


def apply_force(a, b):
    if a == b:
        return

    d2 = (a.x - b.x) ** 2 + (a.y - b.y) ** 2
    if d2 < NODE_RADIUS:
        d2 = NODE_RADIUS
    if d2 > MAX_DIST ** 2:
        return

    dA = COUPLING[a.type - 1][b.type - 1] / d2
    dB = COUPLING[b.type - 1][a.type - 1] / d2
    if a.links < LINKS[a.type - 1] and b.links < LINKS[b.type - 1]:
        if d2 < MAX_DIST ** 2 / 4:
            if b not in a.bonds and a not in b.bonds:
                type_count_a = 0
                for p in a.bonds:
                    if p.type == b.type:
                        type_count_a += 1
                type_count_b = 0
                for p in b.bonds:
                    if p.type == a.type:
                        type_count_b += 1
                if type_count_a < LINKS_POSSIBLE[a.type - 1][b.type - 1] and type_count_b < LINKS_POSSIBLE[b.type - 1][
                    a.type - 1]:
                    a.bonds.append(b)
                    b.bonds.append(a)
                    a.links += 1
                    b.links += 1
                    links.append(Link(a, b))

    elif b not in a.bonds and a not in b.bonds:
        dA = 1 / d2
        dB = 1 / d2

    from math import atan2

    angle = atan2(a.y - b.y, a.x - b.x)
    if d2 < 1:
        d2 = 1
    if d2 < NODE_RADIUS * NODE_RADIUS * 4:
        dA = 1 / d2
        dB = 1 / d2

    a.sx += math.cos(angle) * dA * SPEED
    a.sy += math.sin(angle) * dA * SPEED
    b.sx -= math.cos(angle) * dB * SPEED
    b.sy -= math.sin(angle) * dB * SPEED


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

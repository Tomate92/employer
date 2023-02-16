import pygame, time, sys, random
from pygame.locals import *
from math import *

# pygame.mixer.init(44100, 0, 1024)
pygame.mixer.init()

#pygame.mixer.music.load("lizard.mod")
#pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((800, 600))  # , FULLSCREEN)
#tweet = pygame.mixer.Sound("launch.ogg")
#winlevel = pygame.mixer.Sound("winlevel.wav")


class Level(object):
    def __init__(self, difficulty):
        self.d = difficulty
        self.start_diff = 16
        self.dsize = self.start_diff + int(log(self.d)) * 2
        self.maparray = [[1 for x in range(self.dsize)] for y in range(self.dsize)]

    def generate(self):
        r = random.randint
        dsize = self.dsize
        self.start = [[r(0, dsize - 1), [0, dsize - 1][r(0, 1)]],
                      [[0, dsize - 1][r(0, 1)], r(0, dsize - 1)]][r(0, 1)]

        self.maparray[self.start[0]][self.start[1]] = 2

        self.crawl(self.start)

    def explode(self):
        pass

    def crawl(self, start):
        global checkpoints, diff, ships
        path = []
        dsize = self.dsize
        path.append(start)
        r = random.randint
        dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        lastdi = -1
        limit = 10 * self.dsize
        cc = 0
        every = limit / (diff + 3) * 2
        while cc < limit:
            cc += 1

            pos = [x for x in path[-1]]

            di = r(0, 3)
            if di == lastdi:
                limit += 1
            else:
                pos[0] += dirs[di][0]
                pos[1] += dirs[di][1]

                if pos in path and r(0, 3):
                    limit += 1
                elif pos[0] < 0 or pos[1] < 0:
                    limit += 1
                elif pos[0] == dsize or pos[1] == dsize:
                    limit += 1
                else:
                    path.append(pos)
                    if len(path) == 2:
                        initialangle = [0, -pi / 2, 2 * pi, pi / 2][di]
                        for ship in ships:
                            ship.angle = initialangle
                            ship.inertia = [0, 0]
                    if not (limit - cc) % every and not cc == limit:
                        checkpoints.append(checkpoint(pos[0], pos[1]))

        for x, y in path:
            if [x, y] != start:
                self.maparray[x][y] = 0

        self.maparray[x][y] = 3

    def closeto(self, path):
        c = []
        for x1, y1 in path:
            for x2 in range(-1, 2):
                for y2 in range(-1, 2):
                    c.append([x1 + x2, y1 + y2])
        return c


class PlayerShip(object):
    def __init__(self, colour=(128, 128, 128)):
        self.colour = colour
        self.x = 400
        self.y = 300
        self.points = [(0.001, -15.0), (-15.0, 15.0), (0.001, 5), (15.0, 15.0)]
        self.angle = 0

        self.keys = {"thrust": 0,
                     "left": 0,
                     "right": 0,
                     "reverse": 0, }

        self.inertia = [0, 0]

        self.size = 0.8
        self.tspeed = 0.075
        self.thrustspeed = 0.3

        self.deceleration = 0.95

    def customise(self, control_thrust, control_left, control_right, c_reverse):
        self.controls = [control_thrust, control_left, control_right, c_reverse]

    def handle(self, key, event):
        self.keys[["thrust", "left", "right", "reverse"][self.controls.index(key)]] = event

    def tick(self):
        global smokebits
        if self.keys["left"]: self.angle -= self.tspeed
        if self.keys["thrust"]:
            #            self.size += 0.005
            xthrust = cos(self.angle) * self.thrustspeed
            ythrust = sin(self.angle) * self.thrustspeed
            self.inertia[0] += xthrust
            self.inertia[1] += ythrust
            smokebits.append([self.x + self.size * 9 * cos(self.angle + pi),
                              self.y + self.size * 9 * sin(self.angle + pi),
                              0,
                              self.angle + pi + random.randint(-10, 10) / 100.0,
                              random.randint(0, 3)])
        if self.keys["reverse"]:
            xthrust = cos(self.angle) * self.thrustspeed
            ythrust = sin(self.angle) * self.thrustspeed
            self.inertia[0] -= xthrust
            self.inertia[1] -= ythrust

        if self.keys["right"]: self.angle += self.tspeed

        self.x += self.inertia[0]
        self.y += self.inertia[1]

        self.inertia[0] *= self.deceleration
        self.inertia[1] *= self.deceleration

        self.check_collision()

    def check_collision(self):
        global level, bx, by, ships, checkpoints, ShipWonRace, tweet
        s = 0
        myrect = Rect(0, 0, 50 * self.size, 50 * self.size)
        myrect.center = self.x, self.y

        for c in checkpoints:
            if myrect.collidepoint(c.x * bx + bx / 2, c.y * by + by / 2):
                if self.colour not in c.touched:
                    c.touched.append(self.colour)
                    #tweet.play()

        if self.x <= self.size * 12:
            self.x = self.size * 12 + 1
            self.inertia[0] *= -1
        elif self.x >= 800 - self.size * 12:
            self.x = 800 - self.size * 12 - 1
            self.inertia[0] *= -1
        if self.y <= self.size * 12:
            self.y = self.size * 12 + 1
            self.inertia[1] *= -1
        elif self.y >= 600 - self.size * 12:
            self.y = 600 - self.size * 12 - 1
            self.inertia[1] *= -1

        for x, y in [[self.x, self.y - 12 * self.size],
                     [self.x, self.y + 12 * self.size],
                     [self.x - 12 * self.size, self.y],
                     [self.x + 12 * self.size, self.y]]:

            s += 1
            if x < 0 or x >= 800 or y < 0 or y >= 600:
                continue
            if int(x / bx) >= level.dsize or int(y / by) >= level.dsize:
                continue
            if level.maparray[int(x / bx)][int(y / by)] in [1]:
                if s == 1:
                    self.y = int(y / by) * by + 1 + 12 * self.size + by
                elif s == 2:
                    self.y = int(y / by) * by - 1 - 12 * self.size
                elif s == 3:
                    self.x = int(x / bx) * bx + 1 + 12 * self.size + bx
                elif s == 4:
                    self.x = int(x / bx) * bx - 1 - 12 * self.size

                if s < 3:
                    # Top/bottom
                    self.inertia[1] *= -1
                else:
                    # Left/right
                    self.inertia[0] *= -1
            elif level.maparray[int(x / bx)][int(y / by)] == 3:
                win = True
                for c in checkpoints:
                    if self.colour not in c.touched:
                        win = False

                if win:
                    ShipWonRace = self

    ##             for othership in ships:
    ##                 theirrect.center = othership.x, othership.y
    ##                 if theirrect.collidepoint(x, y):
    ##                     if s == 1:
    ##                         self.y = theirrect.bottom+1+12*self.size
    ##                         othership.y = myrect.top-1-12*othership.size
    ##                         self.inertia, othership.inertia = othership.inertia[:], self.inertia[:]
    ##                     elif s == 2:
    ##                         self.y = theirrect.top-1-12*self.size
    ##                         othership.y = myrect.bottom+1+12*othership.size
    ##                         self.inertia, othership.inertia = othership.inertia[:], self.inertia[:]
    ##                     elif s == 3:
    ##                         self.x = theirrect.right+1+12*self.size
    ##                         othership.x = myrect.left-1-12*othership.size
    ##                         self.inertia, othership.inertia = othership.inertia[:], self.inertia[:]
    ##                     elif s == 4:
    ##                         self.x = theirrect.left-1-12*self.size
    ##                         othership.x = myrect.right+1+12*othership.size
    ##                         self.inertia, othership.inertia = othership.inertia[:], self.inertia[:]

    def initlocation(self, start, bx, by, c):
        self.x = start[0] * bx + bx / 2
        self.y = start[1] * by + by / 2

    def getpoints(self):
        self.rpoints = []
        for x, y in self.points:

            fangle = atan(y / x)
            if x < 0 and y < 0: fangle += pi
            if x < 0 and y > 0: fangle += pi
            fangle += pi / 2
            modulus = sqrt(x ** 2 + y ** 2)
            self.rpoints.append(
                (cos(fangle + self.angle) * self.size * modulus, sin(fangle + self.angle) * self.size * modulus))
        return [(x + self.x, y + self.y) for (x, y) in self.rpoints]


class checkpoint(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.touched = []
        self.colour = (200, 200, 200)

    def tick(self):
        if self.touched:
            if self.colour in self.touched:
                self.colour = self.touched[(self.touched.index(self.colour) + 1) % len(self.touched)]
            else:
                self.colour = self.touched[0]


gamemode = "Race"
checkpoints = []

ships = [PlayerShip((255, 20, 35)), PlayerShip((50, 170, 250)), PlayerShip((240, 20, 220)), PlayerShip((255,170,220))]
smokebits = []

ships[0].customise(K_w, K_a, K_d, K_s)
ships[1].customise(K_UP, K_LEFT, K_RIGHT, K_DOWN)
ships[2].customise(K_o, K_k, K_m, K_l)
ships[3].customise(K_t, K_f, K_h, K_g)

shipnames = ["Red", "Blue", "Pink", "Other"]
scores = dict.fromkeys(shipnames, 0)

diff = int(input("Quelle difficulté pour les niveaux ?"))


def makelevel():
    global level, bx, by, block, rs, diff, ships
    # Background
    screen.fill(0)
    level = Level(diff)
    level.generate()
    bx = 800 / level.dsize
    by = 600 / level.dsize
    block = Rect(0, 0, bx, by)
    rs = []
    drawmap()
    # initialise ships
    sc = 0
    for ship in ships:
        sc += 1
        ship.initlocation(level.start, bx, by, sc)

    pygame.display.flip()


def drawmap():
    c1 = 50
    c2 = 80
    c3 = 150
    for x in range(level.dsize):
        for y in range(level.dsize):
            b = level.maparray[x][y]
            if b == 1:
                screen.fill((c1, c2, c3), block.move(x * bx, y * by))
            elif b == 2:
                screen.fill((50, 230, 60), block.move(x * bx, y * by))
            elif b == 3:
                screen.fill((200, 230, 60), block.move(x * bx, y * by))


def drawcheckpoints():
    global checkpoints, rs, gametick
    for c in checkpoints:
        x = c.x * bx + bx / 2
        y = c.y * by + by / 2
        r = (bx + by) / 8 + sin(gametick / 5.0) * 2
        rs.append(pygame.draw.circle(screen, c.colour, (x, y), r, 0))


makelevel()
gametick = 0
smoke = []
ShipWonRace = None
drawnwin = False

for x in range(3, 10, 2):
    smoke.append(pygame.Surface((x, x)))
    smoke[-1].fill((255, 0, 255))
    smoke[-1].set_colorkey((255, 0, 255))
    c = 160 + x * 10
    pygame.draw.circle(smoke[-1], (c, c, c), (x / 2 + 1, x / 2 + 1), x / 2 + 1, 0)


running=True
while running:
    time.sleep(0.02)
    gametick += 1
    screen.fill(0)
    oldrs = rs[:]
    rs = []
    drawmap()
    drawcheckpoints()

    if not gametick % 10:
        for c in checkpoints:
            c.tick()

    for ship in ships:
        ship.tick()
        sgp = ship.getpoints()
        if ship == ShipWonRace or not ShipWonRace:
            rs.append(pygame.draw.polygon(screen, ship.colour, sgp).inflate(ship.size * 15, ship.size * 15))

    for x, y, d, a, b in smokebits:
        d = min(d, 2)
        rs.append(screen.blit(smoke[b], (x - b, y - b)).inflate(9, 9))

    for t in range(len(smokebits)):
        smokebits[t][2] += 0.25
        if smokebits[t][2] >= 2:
            smokebits[t] = None
            continue
        smokebits[t][0] += cos(smokebits[t][3]) * 2
        smokebits[t][1] += sin(smokebits[t][3]) * 2

    while None in smokebits:
        smokebits.remove(None)

    if ShipWonRace and not drawnwin:
        drawnwin = True
        mysurf = pygame.Surface((1000, 900))
        mysurf.fill(ShipWonRace.colour)
        mysurf.set_colorkey((255, 0, 255))
        pygame.draw.circle(mysurf, (255, 0, 255), (ShipWonRace.x, ShipWonRace.y), 150, 0)
        screen.blit(mysurf, (0, 0))
        pygame.display.flip()
        cw = shipnames[ships.index(ShipWonRace)]
        print(cw, "wins!")
        scores[cw] += 1
        for c, p in scores.items():
            print(c + ":", p)
        #winlevel.play()
        time.sleep(2)

        # Reset for new
        diff += 1
        checkpoints = []
        makelevel()
        ShipWonRace = None
        drawnwin = False

    pygame.display.update(rs + oldrs)
    #    rs = rs[-12:]

    for ev in pygame.event.get():
        if ev.type == KEYDOWN:
            k = ev.key
            for ship in ships:
                if k in ship.controls:
                    ship.handle(k, 1)

            if k == K_ESCAPE:
                sys.exit(0)

        elif ev.type == KEYUP:
            k = ev.key
            for ship in ships:
                if k in ship.controls:
                    ship.handle(k, 0)

        elif ev.type == pygame.QUIT:
            running = False
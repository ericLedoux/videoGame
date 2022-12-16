import pygame as pg # This makes it so that whenever we reference pygame in the code below, we only have to write 'pg'
from pygame.sprite import Sprite
from assets import settings as sett
import os
vec = pg.math.Vector2

# This class is for the player, the ship
class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)

        familiarShip = pg.image.load(os.path.join('assets', 'familiar_ship.png'))
        familiarShip_rect = familiarShip.get_rect()
        familiarShip.set_colorkey(sett.BLACK)
        familiarShip = pg.transform.scale(familiarShip, (90,90))

        self.image = familiarShip
        self.rect = self.image.get_rect()
        self.rect.center = (sett.WIDTH/2, sett.HEIGHT/2)
        self.pos = vec(sett.WIDTH/2, sett.HEIGHT/2) # Position
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        print(self.rect.center)

    def controls(self):
        keys = pg.key.get_pressed() # This is saying "Hey, a key has been pressed".  The lines under define how when we press a certain button, a coorelating action happens
        if keys[pg.K_a]:
            self.acc.x = -5
        if keys[pg.K_d]:
            self.acc.x = 5
        if keys[pg.K_w]:
            self.acc.y = -5
        if keys[pg.K_s]:
            self.acc.y = 5

# these lines make it so that the player teleports to the other side of the screen if they run into the screen borders
        if self.pos.x > sett.WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = sett.WIDTH

        if self.pos.y > sett.HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = sett.HEIGHT

    def update(self):
        self.acc = vec(0, sett.PLAYER_GRAV)
        self.controls()

# makes the controls and their speeed work the way they do
        self.acc.x += self.vel.x * sett.PLAYER_FRIC
        self.acc.y += self.vel.y * sett.PLAYER_FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.center = self.pos


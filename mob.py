import pygame as pg # This makes it so that whenever we reference pygame in the code below, we only have to write 'pg'
from pygame.sprite import Sprite
from assets import settings as sett
vec = pg.math.Vector2

# This class creates mobs, the little guys that the player has to eat(?) up to get points
class Mob(Sprite):
     def __init__(self, x, y, color, velocityX, velocityY):
        Sprite.__init__(self)
        self.image = pg.Surface((25,25))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = vec(velocityX, velocityY)
        self.pos = vec(x, y)
 
     def update(self):
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y
        self.pos.x = self.rect.x
        self.pos.y = self.rect.y

# The code that teleports, same with player
        if self.pos.x > sett.WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = sett.WIDTH

        if self.pos.y > sett.HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = sett.HEIGHT

        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
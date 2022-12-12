########################################################################################################################

'''
SOURCES:
Table 0
https://coderslegacy.com/python/pygame-platformer-game/ (for the screen-looping mechanic)
https://stackoverflow.com/questions/30720665/countdown-timer-in-pygame (for my timer)
'''

########################################################################################################################

'''
THE GOALS OF THE GAME:

To have 2 classes: one for the player and a basic mob.

To have a time limit and a score counter, so that when the time ends the game tells you your score.

To use random to make it so that the mobs spawn in random points (and in random colors/trajectories) across the screen and to code a way to make sure the
player doesn't go off the screen.

'''

########################################################################################################################

# This is where we import our libraries and modules.
import pygame as pg # This makes it so that whenever we reference pygame in the code below, we only have to write 'pg' 
# rather than 'pygame'.
from pygame.sprite import Sprite
import os
from random import randint, random

########################################################################################################################

vec = pg.math.Vector2

# Setting up asset folders here
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')

########################################################################################################################

# Our settings go here (another python convention is all caps for global variables).  Change 'WIDTH' and 'HEIGHT'
# variables to make the screen less/more wide or high.
WIDTH = 1000
HEIGHT = 800
FPS = 30

# player settings
PLAYER_FRIC = -.75
PLAYER_GRAV = 0
POINTS = 0
TIME = 15

# Next, we define colors (with RGB values of course).  Also, these colors are global so we write them in all caps.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

########################################################################################################################

# These lines of code are a class for creating words that you can see on screen
def draw_text(text, size, color, x, y):
        font_name = pg.font.match_font('comic sans')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

########################################################################################################################

# This class is for the player, the big green block
class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pg.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2) 
        self.pos = vec(WIDTH/2, HEIGHT/2) # Position
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
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        self.controls()

# makes the controls and their speeed work the way they do
        self.acc.x += self.vel.x * PLAYER_FRIC
        self.acc.y += self.vel.y * PLAYER_FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.center = self.pos

########################################################################################################################

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

# Same with player on line 98
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT

        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        
########################################################################################################################

class DeathBlock(Sprite):
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

# Same with player on line 98
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT

        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

########################################################################################################################

# And here we intialize the window that we will see the code in.
pg.init() # This line means to, in more human terms, intitialize pygame
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("15-Second Dash!") # This makes the tab name whatever you want it to be

clock = pg.time.Clock()
time_delay = 1000
timer_event = pg.USEREVENT+1
pg.time.set_timer(timer_event, time_delay)

# Creates a group of all sprites that allow us to edit them all at once here rather than editing them one by one
all_sprites = pg.sprite.Group()
mobs = pg.sprite.Group()
all_badguys = pg.sprite.Group()

########################################################################################################################

# Instanciate (instance: an object that belongs to a class) the player and death block
player = Player()

########################################################################################################################

# Add player to all sprites group
all_sprites.add(player)

for i in range(20): # This line creates however many mobs we want to make
    m = Mob(randint(0,WIDTH), randint(0,HEIGHT), ((0), (255) , (0)), randint(-2,2), randint(-2,2)) 
    all_sprites.add(m)
    mobs.add(m)
print(mobs)

for i in range(10): # This line creates however many mobs we want to make
    bg = DeathBlock(randint(0,WIDTH), randint(0,HEIGHT), ((255), (0) , (0)), randint(-2,2), randint(-2,2)) 
    all_sprites.add(bg)
    all_badguys.add(bg)
print(all_badguys)

########################################################################################################################

# The game loop begins here.
running = True
while running:
    # This following line keeps the loop, well, looping using the clock.
    clock.tick(FPS)
    # This 'for' loop checks to see if the user pressed the red 'x' on the window.
    for event in pg.event.get():
        if event.type == pg.QUIT:
            # Line 34 will break the loop, as the action being performed by the user (pressing the red 'x') will end the 
            # program, and therefore the loop. 
            running = False
        elif event.type == timer_event:
            if TIME > 0:
                TIME -= 1
            if TIME == 0:
                all_sprites.empty()
                all_badguys.empty()
                
########################################################################################################################

    ############### Update ###############

    # Updates all sprites
    all_sprites.update()

    mobhits = pg.sprite.spritecollide(player, mobs, True)
    if mobhits:
        POINTS += 1
    all_sprites.update()

    dbhits = pg.sprite.spritecollide(player, all_badguys, True)
    if dbhits:
        TIME = 0
    all_sprites.update()

    if mobhits:
        m = Mob(randint(0,WIDTH), randint(0,HEIGHT), ((0), (255) , (0)), randint(-2,2), randint(-2,2)) 
        all_sprites.add(m)
        mobs.add(m)

    if dbhits:
        bg = DeathBlock(randint(0,WIDTH), randint(0,HEIGHT), ((255), (0) , (0)), randint(-2,2), randint(-2,2)) 
        all_sprites.add(bg)
        all_badguys.add(bg)

    ############### Draw ###############

        # Draws the background screen
    screen.fill(BLACK)

    draw_text("POINTS: " + str(POINTS) + "   " + "TIME: " + str(TIME), 22, WHITE, WIDTH / 2, HEIGHT / 24)
    if TIME <= 0:
          draw_text("GAME OVER!", 50, WHITE, WIDTH / 2, HEIGHT / 2)
        # Draws all sprites
    all_sprites.draw(screen)
    all_badguys.draw(screen)

    # This is a buffer that makes it so after the code has drawn everything, the display will be flipped; updated is a better way to put it (think 'flip' as in 'flipbook'). 
    pg.display.flip() # This will flip the displays.

pg.quit()
########################################################################################################################
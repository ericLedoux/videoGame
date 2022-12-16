########################################################################################################################

'''
SOURCES:
Table 0
https://coderslegacy.com/python/pygame-platformer-game/ (for the screen-looping mechanic)
https://stackoverflow.com/questions/30720665/countdown-timer-in-pygame (for my timer)
https://stackoverflow.com/questions/5055042/whats-the-best-practice-using-a-settings-file-in-python (for settings)
https://gist.github.com/ogilviemt/9b05a89d023054e6279f (for the starfield background)

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

from assets import settings as sett

from player import Player

from mob import Mob

from deathblock import DeathBlock

# rather than 'pygame'.
from pygame.sprite import Sprite

import os

from random import randint, random

########################################################################################################################

# local variables
time_remaining = 60
point_score = 0

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

star_field_slow = []
star_field_medium = []
star_field_fast = []

for slow_stars in range(30):
    star_loc_x = randint(0, sett.WIDTH)
    star_loc_y = randint(0, sett.HEIGHT)
    star_field_slow.append([star_loc_x, star_loc_y])

for medium_stars in range(20):
    star_loc_x = randint(0, sett.WIDTH)
    star_loc_y = randint(0, sett.HEIGHT)
    star_field_medium.append([star_loc_x, star_loc_y])

for fast_stars in range(10):
    star_loc_x = randint(0, sett.WIDTH)
    star_loc_y = randint(0, sett.HEIGHT)
    star_field_fast.append([star_loc_x, star_loc_y])

########################################################################################################################

# And here we intialize the window that we will see the code in.
pg.init() # This line means to, in more human terms, intitialize pygame
pg.mixer.init()
screen = pg.display.set_mode((sett.WIDTH, sett.HEIGHT))
pg.display.set_caption("60-Second Dash!") # This makes the tab name whatever you want it to be

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

for i in range(sett.MOB_COUNT): # This line creates however many mobs we want to make
    m = Mob(randint(0,sett.WIDTH), randint(0,sett.HEIGHT), ((0), (255) , (0)), randint(-2,2), randint(-2,2))
    all_sprites.add(m)
    mobs.add(m)
print(mobs)

for i in range(sett.DEATH_BLOCK_COUNT): # This line creates however many mobs we want to make
    bg = DeathBlock(randint(0,sett.WIDTH), randint(0,sett.HEIGHT), ((255), (0) , (0)), randint(-2,2), randint(-2,2))
    all_sprites.add(bg)
    all_badguys.add(bg)
print(all_badguys)

########################################################################################################################

# The game loop begins here.
running = True
while running:
    # This following line keeps the loop, well, looping using the clock.
    clock.tick(sett.FPS)
    # This 'for' loop checks to see if the user pressed the red 'x' on the window.
    for event in pg.event.get():
        if event.type == pg.QUIT:
            # Line 34 will break the loop, as the action being performed by the user (pressing the red 'x') will end the
            # program, and therefore the loop.
            running = False
        elif event.type == timer_event:
            if time_remaining > 0:
                time_remaining -= 1
            if time_remaining == 0:
                all_sprites.empty()
                all_badguys.empty()

########################################################################################################################

    ############### Update ###############

    # Updates all sprites

    all_sprites.update()

    mobhits = pg.sprite.spritecollide(player, mobs, True)
    if mobhits:
        point_score += 1
    all_sprites.update()

    dbhits = pg.sprite.spritecollide(player, all_badguys, True)
    if dbhits:
        time_remaining = 0
    all_sprites.update()

    if mobhits:
        m = Mob(randint(0,sett.WIDTH), randint(0,sett.HEIGHT), ((0), (255) , (0)), randint(-2,2), randint(-2,2))
        all_sprites.add(m)
        mobs.add(m)

    if dbhits:
        bg = DeathBlock(randint(0,sett.WIDTH), randint(0,sett.HEIGHT), ((255), (0) , (0)), randint(-2,2), randint(-2,2))
        all_sprites.add(bg)
        all_badguys.add(bg)

    ############### Draw ###############

        # Draws the background screen
    screen.fill(sett.BLACK)

    draw_text("POINTS: " + str(point_score) + "   " + "TIME: " + str(time_remaining), 22, sett.WHITE, sett.WIDTH / 2, sett.HEIGHT / 24)
    if time_remaining <= 0:
          draw_text("GAME OVER!", 50, sett.WHITE, sett.WIDTH / 2, sett.HEIGHT / 2)
          draw_text("Your point count was: "+ str(point_score) + "!", 40, sett.WHITE, sett.WIDTH / 2, sett.HEIGHT / 1.75)
        # Draws all sprites
    all_sprites.draw(screen)
    all_badguys.draw(screen)

    # This is the code that draws the moving stars in the background
    for star in star_field_slow:
        star[1] += 1
        if star[1] > sett.HEIGHT:
            star[0] = randint(0, sett.WIDTH)
            star[1] = randint(-20, -5)
        pg.draw.circle(screen, sett.DARK_GREY, star, 3)

    for star in star_field_medium:
        star[1] += 2
        if star[1] > sett.HEIGHT:
            star[0] = randint(0, sett.WIDTH)
            star[1] = randint(-20, -5)
        pg.draw.circle(screen, sett.LIGHT_GREY, star, 2)

    for star in star_field_fast:
        star[1] += 3
        if star[1] > sett.HEIGHT:
            star[0] = randint(0, sett.WIDTH)
            star[1] = randint(-20, -5)
        pg.draw.circle(screen, sett.YELLOW, star, 1)

    # This is a buffer that makes it so after the code has drawn everything, the display will be flipped; updated is a better way to put it (think 'flip' as in 'flipbook').
    pg.display.flip() # This will flip the displays.
pg.quit()

########################################################################################################################
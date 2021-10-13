from pygame import image, time, event, font
import pygame
from os import path
from setup import window, update
splashImage = image.load(path.join("splash.png"))
# The sole purpose of this script is to make the intro screen
menu = True
cursor_pos = 0
boxPositions = {0: 200, 1: 500}
font.init()
text = font.SysFont('Arial', 36, False, False)
single = text.render('Singleplayer (Currently the same as Multiplayer)', False, (0, 0, 0))
multi = text.render('Multiplayer', False, (0, 0, 0))


def up():
    global cursor_pos
    if cursor_pos != 0:
        cursor_pos = 0


def down():
    global cursor_pos
    if cursor_pos != 1:
        cursor_pos = 1


def set_game_mode(mode):
    pass


def start_screen():
    for t in xrange(0, 400):
        try:
            window.fill((255, 255, 255))
            window.blit(splashImage, (0, 0))
            update()
            time.delay(1)
        except:
            break
    window.fill((255, 255, 255))
    update()
    while menu is True:
        try:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pygame.display.toggle_fullscreen()
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        up()
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        down()
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_RETURN:  # for now, there is only one option for this (multi player),
                        # which will be the bottom option
                        if cursor_pos == 1:
                            set_game_mode(2)
                        elif cursor_pos == 0:
                            set_game_mode(1)
                        quit(splash)
            window.fill((255, 255, 255))
            window.blit(single, (350, 180))
            window.blit(multi, (350, 480))
            pygame.draw.rect(window, (0, 0, 0), (300, boxPositions[cursor_pos], 10, 10))
            update()
        except:
            break

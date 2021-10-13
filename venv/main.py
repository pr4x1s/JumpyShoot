import os
import pygame
import threading
import sys
#file_dir = path.dirname(__file__)
#sys.path.append(file_dir)
#print(file_dir)


scriptpath = "/home/dominik/Desktop/School/Github_Code/Jumpy_Shoot/venv/"

# Add the directory containing your module to the Python path (wants absolute paths)
sys.path.append(os.path.abspath(scriptpath))

import setup
import ground
import player
import splash
import bullet



from pygame.locals import *
WHITE = (255, 255, 255)
clock = pygame.time.Clock()
g1 = ground.Ground(175, 300)
g6 = ground.Ground(175, 500)
g2 = ground.Ground(175, 700)
g3 = ground.Ground(175, 100)
g4 = ground.Ground(1050, 300)
g5 = ground.Ground(1050, 500)
g7 = ground.Ground(1050, 700)
g8 = ground.Ground(1050, 100)
g9 = ground.Ground(500, 600)
# To-do to make this a completed game:
# Fix the scoreboard (make it look nicer, especially red team)
# Make an actual map
# Fix the 'double score' glitch, either by making a variable that detects a jump in the score or other wise
# like 'if last score was even but this one isn't, subtract one from the score'
# ADD A DEATH AND RE-SPAWN ANIMATION
# Make a main menu
# Put the current music for the main menu, 'Battle Music' will be used during battle
# --------------------------------------------------------------------
bluePlayer = player.Player("blue")
redPlayer = player.Player("red")
# Here is the main loop - will handle everything like event handling and calls to other functions and stuff
pygame.key.set_repeat()
done = False


def score_check():
    while mainLoop.isAlive() is True:
        print("Current score: %d Last Score: %d" % (redPlayer.score, redPlayer.lastScore))
        if bluePlayer.score == bluePlayer.lastScore + 2:
            bluePlayer.score -= 1
        if bluePlayer.score == bluePlayer.lastScore + 1:
            bluePlayer.lastScore = bluePlayer.score
        if redPlayer.score == redPlayer.lastScore + 2:
            redPlayer.score -= 1
        if redPlayer.score == redPlayer.lastScore + 1:
            redPlayer.lastScore = redPlayer.score
        pygame.time.wait(100)


def blueloop():
    try:
        lastBlueKey = {pygame.K_a: False, pygame.K_d: True}
        global done
        while done is False:
            clock.tick(60)
            keys = pygame.key.get_pressed()
            if startLoop.isAlive() is False:
                # Blue player's keys:
                if keys[K_a]:
                    bluePlayer.move(-2, 0)
                    bluePlayer.last_key(lastBlueKey[pygame.K_a])
                if keys[K_d]:
                    bluePlayer.move(2, 0)
                    bluePlayer.last_key(lastBlueKey[pygame.K_d])

                # --------------------
    except:
        quit()


def redloop():
    try:
        lastRedKey = {pygame.K_LEFT: False, pygame.K_RIGHT: True}
        global done
        while done is False:
            clock.tick(60)
            keys = pygame.key.get_pressed()
            # Red player's keys:
            if startLoop.isAlive() is False:
                if keys[K_LEFT]:
                    redPlayer.move(-2, 0)
                    redPlayer.last_key(lastRedKey[pygame.K_LEFT])
                if keys[K_RIGHT]:
                    redPlayer.move(2, 0)
                    redPlayer.last_key(lastRedKey[pygame.K_RIGHT])
            # ----------------------------
    except:
        quit()


def main():
    score_check_loop.start()
    blueLoop.start()
    redLoop.start()
    global done
    while done is False:
        clock.tick(60)
        try:  # try-statement is used here in case the user quits in the main menu
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = True
                    if event.key == pygame.K_p:
                        pygame.display.toggle_fullscreen()
                    if event.key == pygame.K_LSHIFT and startLoop.isAlive() is False:
                        bluePlayer.shoot()
                        channel.play(shootSound)
                    if event.key == pygame.K_RCTRL and startLoop.isAlive() is False:
                        redPlayer.shoot()
                        channel.play(shootSound)
                    if event.key == pygame.K_w and startLoop.isAlive() is False and bluePlayer.jumping is False \
                            and bluePlayer.onPlatform is True:
                        bluePlayer.jumping = True
                        pygame.time.wait(1)
                    if event.key == pygame.K_UP and startLoop.isAlive() is False and redPlayer.jumping is False \
                            and redPlayer.onPlatform is True:
                        redPlayer.jumping = True
                        pygame.time.wait(1)
        except ZeroDivisionError:
            break
        if startLoop.isAlive() is False:
            setup.window.fill(WHITE)
            bluePlayer.blit()
            redPlayer.blit()
            if bluePlayer.jumping is True:
                x = bluePlayer.upwardsMomentum
                y = -.04 * (x - 16)**2 + 10
                bluePlayer.ypos -= int(y)
                bluePlayer.upwardsMomentum += 1
            else:
                bluePlayer.calc_vel()
            if bluePlayer.upwardsMomentum > 32:
                bluePlayer.jumping = False
                bluePlayer.upwardsMomentum = 0
            if redPlayer.jumping is True:
                x = redPlayer.upwardsMomentum
                y = -.04 * (x - 16) ** 2 + 10
                redPlayer.ypos -= int(y)
                redPlayer.upwardsMomentum += 1
            else:
                redPlayer.calc_vel()
            if redPlayer.upwardsMomentum > 32:
                redPlayer.jumping = False
                redPlayer.upwardsMomentum = 0
            for gInstance in ground.instances:
                gInstance.blit()
            bullet.Bullet.blit()
            bluePlayer.display_score()
            redPlayer.display_score()
            setup.update()
    pygame.quit()
    quit()


if __name__ == "__main__":
    pygame.init()
    shootSound = pygame.mixer.Sound(os.path.join("pew.ogg"))
    shootSound.set_volume(1)
    channel = pygame.mixer.Channel(1)
    pygame.mixer.music.load(os.path.join("Lil' Nagen - Jumpy Shoot Soundtrack (original).ogg"))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(.6)
    mainLoop = threading.Thread(target=main)
    startLoop = threading.Thread(target=splash.start_screen)
    blueLoop = threading.Thread(target=blueloop)
    redLoop = threading.Thread(target=redloop)
    score_check_loop = threading.Thread(target=score_check)
    startLoop.start()
    startLoop.join()
    mainLoop.start()


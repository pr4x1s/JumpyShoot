from os import path
from pygame import image, transform, font
from threading import Thread
from setup import window
import bullet
import ground
players = []
font.init()


class Player:
    def __init__(self, team):
        global players
        players.append(self)
        self.team = team
        self.score = 0
        self.lastScore = self.score
        # 0 he is facing the right, 1 he is facing the left
        self.BlueTeamImages = (image.load(path.join("jumpy_shoot_blue.png")), transform.flip(image.load(path.join("jumpy_shoot_blue.png")), True, False))
        self.RedTeamImages = (image.load(path.join("jumpy_shoot_red.png")), transform.flip(image.load(path.join("jumpy_shoot_red.png")), True, False))
        self.currentVel = 0
        self.jumping = False
        self.onPlatform = False
        self.upwardsMomentum = 0
        self.text = font.SysFont('Arial', 24, False, False)
        self.yVel = 0

        # These will have to change before I start blitting them to the screen
        if team == "blue":
            self.isFacingRight = True
            self.xpos = 200
            self.ypos = 200
        elif team == "red":
            self.isFacingRight = False
            self.xpos = 1080
            self.ypos = 200
        else:
            raise TypeError("Input for Player object needs to be either 'red' or 'blue'")

    def move(self, xchange, ychange):
        self.xpos += xchange
        self.ypos += ychange
# Calc-fall and calc-vel are meant to calculate the velocity and/or falling rate of the player
# These can probably be kept as separate function, but I should make a thread that will run calc_fall()

    def blit(self):
        if self.team == "blue":
            if self.isFacingRight is True:
                window.blit(self.BlueTeamImages[0], (self.xpos, self.ypos))
            else:
                window.blit(self.BlueTeamImages[1], (self.xpos, self.ypos))
        else:
            if self.isFacingRight is True:
                window.blit(self.RedTeamImages[0], (self.xpos, self.ypos))
            else:
                window.blit(self.RedTeamImages[1], (self.xpos, self.ypos))
                
    def calc_fall(self, instancetouched):
        if instancetouched.is_touching(self) is False:
            self.yVel += .15
            self.ypos += self.yVel

    def calc_vel(self):
        maxVel = 1
        for i in ground.instances:
            if i.is_touching(self) is True:
                self.yVel = 0
                self.currentVel = 0
                self.setpos(self.xpos, i.ypos - 45)
                self.onPlatform = True
                break
            else:
                self.onPlatform = False
                if self.yVel <= maxVel:
                    self.yVel += .02
                self.ypos += self.yVel
        if self.ypos > 720:
            self.ypos = -10

    def shoot(self):
        #shootingSound.play()
        bullet.bInstances.append(bullet.Bullet((self.xpos, self.ypos + 18), self.isFacingRight, self.team))
        lastBulletIndex = len(bullet.bInstances) - 1
        bullet.bInstances[lastBulletIndex].moving()

    def last_key(self, key):
        self.isFacingRight = key
        
    def setpos(self, x, y):
        self.xpos = x
        self.ypos = y

    def display_score(self):
        if self.team == 'blue':
            color = (0, 0, 240)
            pos = (30, 20)
        else:
            color = (240, 0, 0)
            pos = (1230, 20)
        text = self.text.render(str(self.score), True, color)
        window.blit(text, pos)

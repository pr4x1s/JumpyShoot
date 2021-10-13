# This class will have the following information to define a 'bullet'
"""
direction - True is right, False is left
velocity - speed of the bullet
width and height - will be used to create the hit box of the bullet
costume - might have different costumes, although this depends on whether or not I add upgrades
"""
from setup import window
from pygame import image, transform
from os import path
import player
bInstances = []


class Bullet:
    def __init__(self, startpos, direction, firedby):
        self.x = startpos[0]
        self.y = startpos[1]
        self.velocity = 0
        # If direction is True, that means that it is facing left
        # And vice versa
        self.direction = direction
        self.firedby = firedby
        # Add an image of a bullet, then transform it
        self.image = image.load(path.join("bullet.png"))
        self.fired = False
        self.hit = False
        self.index = len(bInstances) - 1
        self.usedUp = False
        
    def collision(self):
        bluePlayer = player.players[0]
        redPlayer = player.players[1]
        is_true = False
        if self.firedby == 'blue':
            if self.x >= redPlayer.xpos and self.x <= redPlayer.xpos + 13 and self.y >= redPlayer.ypos \
            and self.y <= redPlayer.ypos + 45:
                bluePlayer.score += 1
                is_true = True
                print('Red Hit!')
                self.hit = True
        else:
            if self.x >= bluePlayer.xpos and self.x <= bluePlayer.xpos + 13 and self.y >= bluePlayer.ypos \
            and self.y <= bluePlayer.ypos + 45:
                if redPlayer.onPlatform is False:
                    pass
                redPlayer.score += 1
                is_true = True
                print('Blue Hit!')
                self.hit = True
        if is_true:
            try:
                del bInstances[self.index]
            except IndexError:
                pass

    def moving(self):
        self.fired = True
        if self.direction is True:
            self.velocity = 10
        else:
            self.velocity = -10

    @staticmethod
    def blit():
        for instance in bInstances:
            if instance.x > 1280 or instance.x < 0:
                del instance
                continue
            if instance.fired:
                instance.x += instance.velocity
                window.blit(instance.image, (instance.x, instance.y))
                instance.collision()
                if instance.hit is True:
                    del instance
                    continue




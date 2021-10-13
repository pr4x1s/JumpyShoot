from setup import window
from pygame import image
from os import path
instances = []


class Ground:
    def __init__(self, x, y):
        global instances
        instances.append(self)
        self.xpos = x
        self.ypos = y
        self.image = image.load(path.join("ground.png"))
        
    def is_touching(self, player_instance):
        playerWidth = 13
        playerHeight = 45
        if player_instance.xpos + playerWidth >= self.xpos and player_instance.xpos <= self.xpos + 50 \
                and player_instance.ypos + playerHeight >= self.ypos and player_instance.ypos + playerHeight <= self.ypos + 10:
            player_instance.yVel = 0
            return True
        else:
            return False
            
    def blit(self):
        window.blit(self.image, (self.xpos, self.ypos))
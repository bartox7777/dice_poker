import os
import pygame
from pygame.sprite import Sprite


pygame.init()


class Die(Sprite):
    def __init__(self, die_number=1, x=0, y=0):
        super().__init__()  # Sprite.__init__(self)
        self.die_number = die_number
        if die_number not in range(1, 7):
            raise Exception("die_number must be between 1 and 6")
        dice_images = [os.path.join("data", "die_{}.png".format(i+1)) for i in range(6)]
        try:
            self.die = pygame.image.load(dice_images[die_number-1])
        except:
            raise Exception("Couldn't load image {}".format(dice_images[die_number-1]))
        self.die_rect = self.die.get_rect(x=x, y=y)
        print(self.die_rect)

    def draw(self, screen, x=None, y=None):
        if x is not None:
            self.die_rect.x = x
        if y is not None:
            self.die_rect.y = y
        screen.blit(self.die, self.die_rect)

    def __repr__(self):
        return "Die {}".format(self.die_number)
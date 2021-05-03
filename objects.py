import os
import pygame
from pygame.sprite import Sprite, Group, GroupSingle


pygame.init()

class Die(Sprite):
    def __init__(self, die_number, x=0, y=0):
        super().__init__()
        self.die_number = die_number

        if die_number not in range(1, 7):
            raise Exception("die_number must be between 1 and 6")
        dice_images = [os.path.join("data", "die_{}.png".format(i+1)) for i in range(6)]

        try:
            self.image = pygame.image.load(dice_images[die_number-1]).convert_alpha()
        except:
            raise Exception("Couldn't load image {}".format(dice_images[die_number-1]))

        self.rect = self.image.get_rect(x=x, y=y)

    def __repr__(self):
        return "Die {}".format(self.die_number)


class Dice(Group):
    def __init__(self):
        super().__init__()


class Table(Sprite):
    def __init__(self, surface, color, topleft_x, topleft_y, width, height):
        super().__init__()
        self.surface = surface
        self.color = color
        self.topleft_x = topleft_x
        self.topleft_y = topleft_y
        self.width = width
        self.height = height
    
    def draw(self):
        pygame.draw.rect(self.surface, self.color, pygame.Rect(self.topleft_x, self.topleft_y, self.width, self.height))


# class TableGroup(GroupSingle):
#     def __init__(self):
#         super().__init__()

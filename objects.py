import os
import pygame
from pygame import draw
from pygame.math import Vector2
from pygame.sprite import Sprite, Group


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
    def __init__(self, surface, color, topleft_x, topleft_y, width, height, players=2):
        super().__init__()
        self.surface = surface
        self.color = color
        self.topleft_x = topleft_x
        self.topleft_y = topleft_y
        self.width = width
        self.height = height

    def draw(self):
        BLACK = (0, 0, 0)
        PADDING = self.width/50
        BOLD_VERTICAL_LINES = [0, 8, 16]
        BOLDER_VERTICAL_LINES = [6, 7, 15]
        INFOS = ["1", "2", "3", "4", "5", "6", "BONUS", "SUM", "TRIPLET", "QUARTET", "FULL HOUSE", "MINI SERIE", "MAXI SERIE", "KNIFFEL", "CHANCE", "SUM", "TOTAL"]

        draw.rect(self.surface, self.color, pygame.Rect(self.topleft_x, self.topleft_y, self.width, self.height))
        vertical_line_space = int(self.height/18)
        vertical_line_start = Vector2(self.topleft_x+PADDING, self.topleft_y)
        vertical_line_end = Vector2(self.topleft_x+self.width-PADDING, self.topleft_y)

        font = pygame.font.Font(None, int(self.width/15))
        texts = [font.render(info, 1, BLACK) for info in INFOS]

        offset = Vector2(0, 0)
        max_text_x = 0
        for i in range(17):
            offset.y += vertical_line_space
            text = texts[i]
            text_pos = text.get_rect(topleft=(self.topleft_x+PADDING+10, vertical_line_start.y+offset.y+10))
            if text_pos.topright[0] > max_text_x: # where to draw first horizontal line
                max_text_x = text_pos.topright[0]
            self.surface.blit(text, text_pos)

            if i in BOLDER_VERTICAL_LINES:
                draw.line(self.surface, BLACK, vertical_line_start+offset, vertical_line_end+offset, 2)
            elif i in BOLD_VERTICAL_LINES:
                draw.line(self.surface, BLACK, vertical_line_start+offset, vertical_line_end+offset, 3)
            else:
                draw.line(self.surface, BLACK, vertical_line_start+offset, vertical_line_end+offset)

        horizontal_line_start = Vector2(max_text_x+10, self.topleft_y+PADDING)
        horizontal_line_end = Vector2(max_text_x+10, self.topleft_y+self.height-PADDING)
        draw.line(self.surface, BLACK, horizontal_line_start, horizontal_line_end)

        # from "players" to "total" row
        points_x_start = max_text_x
        points_y_start = self.topleft_y+PADDING
        points_width = self.width - (max_text_x - self.topleft_x)
        print(points_x_start, points_y_start, points_width)

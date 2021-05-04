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


# class VerticalPlayerRectsWithPoints:
#     def __init__(self)


class Table(Sprite):
    def __init__(self, surface, color, topleft_x, topleft_y, width, height, players=4):
        GREY = (50, 50, 50)

        super().__init__()
        self.surface = surface
        self.color = color
        self.topleft_x = topleft_x
        self.topleft_y = topleft_y
        self.width = width
        self.height = height
        self.players = players
        self.font = pygame.font.Font(None, int(self.width/20))

        self.__INFOS = ["1", "2", "3", "4", "5", "6", "BONUS", "SUM", "TRIPLET", "QUARTET", "FULL HOUSE", "MINI SERIE", "MAXI SERIE", "KNIFFEL", "CHANCE", "SUM", "TOTAL"]

        self.players_points = []
        self.texts_players_points = []
        for _ in range(self.players):
            self.players_points.append([0] * len(self.__INFOS))
            self.texts_players_points.append([self.font.render("0", 1, GREY)] * len(self.__INFOS))

    def draw(self):
        BLACK = (0, 0, 0)
        PADDING = self.width/50
        BOLD_HORIZONTAL_LINES = [0, 8, 16]
        BOLDER_HORIZONTAL_LINES = [6, 7, 15]
        VERTICAL_TEXT_OFFSET = self.width/15

        # DRAWING HORIZONTAL LINES AND PRINTING INFOS

        draw.rect(self.surface, self.color, pygame.Rect(self.topleft_x, self.topleft_y, self.width, self.height))
        horizontal_line_space = int(self.height/18)
        horizontal_line_start = Vector2(self.topleft_x+PADDING, self.topleft_y)
        horizontal_line_end = Vector2(self.topleft_x+self.width-PADDING, self.topleft_y)

        texts = [self.font.render(info, 1, BLACK) for info in self.__INFOS]

        offset = Vector2(0, 0)
        max_text_x = 0
        for i in range(17):
            offset.y += horizontal_line_space
            text = texts[i]
            text_pos = text.get_rect(topleft=(self.topleft_x+PADDING+10, horizontal_line_start.y+offset.y+10))
            if text_pos.topright[0] > max_text_x: # where to draw first vertical line
                max_text_x = text_pos.topright[0]
            self.surface.blit(text, text_pos)

            if i in BOLDER_HORIZONTAL_LINES:
                draw.line(self.surface, BLACK, horizontal_line_start+offset, horizontal_line_end+offset, 2)
            elif i in BOLD_HORIZONTAL_LINES:
                draw.line(self.surface, BLACK, horizontal_line_start+offset, horizontal_line_end+offset, 3)
            else:
                draw.line(self.surface, BLACK, horizontal_line_start+offset, horizontal_line_end+offset)

        # DRAWING VERTICAL LINES AND PRINTING PLAYERS WITH POINTS

        vertical_line_start = Vector2(max_text_x+10, self.topleft_y+PADDING)
        vertical_line_end = Vector2(max_text_x+10, self.topleft_y+self.height-PADDING)

        # from "players" row to "total" row
        points_x_start = max_text_x
        points_y_start = self.topleft_y+PADDING
        points_width = self.width - (max_text_x - self.topleft_x)
        column_width_per_player = points_width / self.players
        row_height = horizontal_line_space


        texts_points_pos = []
        for _ in range(self.players):
            texts_points_pos.append([])

        i = 0
        offset = Vector2(0, 0)
        for player_texts in self.texts_players_points:
            for text in player_texts:
                offset.y += row_height
                texts_points_pos[i].append(text.get_rect(topleft=(points_x_start+offset.x+VERTICAL_TEXT_OFFSET, points_y_start+offset.y)))
            offset.y = 0
            offset.x += column_width_per_player
            i += 1

        for player_texts, player_texts_pos in zip(self.texts_players_points, texts_points_pos):
            for player_text, player_text_pos in zip(player_texts, player_texts_pos):
                self.surface.blit(player_text, player_text_pos)

        offset = Vector2(0, 0)
        for i in range(self.players):
            draw.line(self.surface, BLACK, vertical_line_start+offset, vertical_line_end+offset)

            text = self.font.render("#{}".format(i+1), 1, BLACK)
            text_pos = text.get_rect(topleft=(points_x_start+offset.x+VERTICAL_TEXT_OFFSET, points_y_start))

            self.surface.blit(text, text_pos)
            offset.x += column_width_per_player

    def update(self): # updating points
        pass



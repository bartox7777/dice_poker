import os
import pygame
from pygame import draw
from pygame.math import Vector2
from pygame.sprite import Sprite, Group


pygame.init()

class Die(Sprite):
    def __init__(self, die_number, x=0, y=0, blocked=False):
        super().__init__()
        self.die_number = die_number
        self.blocked = blocked
        self.x = x
        self.y = y

        if die_number not in range(1, 7):
            raise Exception("die_number must be between 1 and 6")
        self.dice_images = [os.path.join("data", "die_{}.png".format(i+1)) for i in range(6)]
        self.dice_images_reversed = [os.path.join("data", "die_{}_reversed.png".format(i+1)) for i in range(6)]
        # DRY!
        if self.blocked:
            try:
                self.image = pygame.image.load(self.dice_images_reversed[self.die_number-1]).convert_alpha()
            except:
                raise Exception("Couldn't load image {}".format(self.dice_images_reversed[self.die_number-1]))
        else:
            try:
                self.image = pygame.image.load(self.dice_images[self.die_number-1]).convert_alpha()
            except:
                raise Exception("Couldn't load image {}".format(self.dice_images[self.die_number-1]))

        self.rect = self.image.get_rect(x=x, y=y)

    def change_state(self):
        self.blocked = not self.blocked
        # DRY!
        if self.blocked:
            try:
                self.image = pygame.image.load(self.dice_images_reversed[self.die_number-1]).convert_alpha()
            except:
                raise Exception("Couldn't load image {}".format(self.dice_images_reversed[self.die_number-1]))
        else:
            try:
                self.image = pygame.image.load(self.dice_images[self.die_number-1]).convert_alpha()
            except:
                raise Exception("Couldn't load image {}".format(self.dice_images[self.die_number-1]))

    def __repr__(self):
        return "Die {}".format(self.die_number)


class Dice(Group):
    def __init__(self):
        super().__init__()


class Table(Sprite):
    def __init__(self, surface, color, topleft_x, topleft_y, width, height, players):
        GREY = (120, 120, 120)

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
        self.UNCLICKABLE_POINTS = [6, 7, 15, 16]

        self.texts_points_pos = []

        self.players_points = []
        self.texts_players_points = []
        self.blocked_points = []
        for _ in range(self.players):
            self.players_points.append([0] * len(self.__INFOS))
            self.texts_players_points.append([self.font.render("0", 1, GREY)] * len(self.__INFOS))
            self.blocked_points.append([False] * len(self.__INFOS))

    def points_to_text(self):
        GREY = (120, 120, 120)
        RED = (255, 0, 0)
        for i in range(self.players):
            for j in range(len(self.__INFOS)):
                if not self.blocked_points[i][j] or j in self.UNCLICKABLE_POINTS:
                    self.texts_players_points[i][j] = self.font.render(str(self.players_points[i][j]), 1, GREY)
                else:
                    self.texts_players_points[i][j] = self.font.render(str(self.players_points[i][j]), 1, RED)

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
        for i in range(len(self.__INFOS)):
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


        for _ in range(self.players):
            self.texts_points_pos.append([])

        i = 0
        offset = Vector2(0, 0)
        for player_texts in self.texts_players_points:
            for text in player_texts:
                offset.y += row_height
                self.texts_points_pos[i].append(text.get_rect(topleft=(points_x_start+offset.x+VERTICAL_TEXT_OFFSET, points_y_start+offset.y)))

            offset.y = 0
            offset.x += column_width_per_player
            i += 1

        for player_texts, player_texts_pos in zip(self.texts_players_points, self.texts_points_pos):
            for player_text, player_text_pos in zip(player_texts, player_texts_pos):
                self.surface.blit(player_text, player_text_pos)

        offset = Vector2(0, 0)
        for i in range(self.players):
            draw.line(self.surface, BLACK, vertical_line_start+offset, vertical_line_end+offset)

            text = self.font.render("#{}".format(i+1), 1, BLACK)
            text_pos = text.get_rect(topleft=(points_x_start+offset.x+VERTICAL_TEXT_OFFSET, points_y_start))

            self.surface.blit(text, text_pos)
            offset.x += column_width_per_player

    # update points and catch point hover
    def update(self, dice_group, player_move, mouse_pos):
        GREEN = (110, 160, 100)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        GREY = (120, 120, 120)

        # count points from roll
        temp_points = self.players_points[player_move-1].copy()
        player_points = self.players_points[player_move-1]
        player_blocked_points = self.blocked_points[player_move-1]

        dice = dice_group.sprites()
        dice_numbers = [die.die_number for die in dice]
        for i in range(len(temp_points)):
            if i not in self.UNCLICKABLE_POINTS and not player_blocked_points[i]:
                # python switch..case please <3 #
                # 1 - 6
                if i in range(6):
                    for j in range(6):
                        sum_of_specific_dots = dice_numbers.count(j+1) * (j+1)
                        temp_points[j] = sum_of_specific_dots

                # TRIPLET and QUARTET
                if i in [8, 9]:
                    for die_number in set(dice_numbers):
                        if dice_numbers.count(die_number) >= 3:
                            temp_points[8] = sum(dice_numbers)
                        if dice_numbers.count(die_number) >= 4:
                            temp_points[9] = sum(dice_numbers)

                # FULL HOUSE (3+2x)
                if i == 10:
                    set_dice_numbers = set(dice_numbers)
                    if len(set_dice_numbers) == 2:
                        if dice_numbers.count(set_dice_numbers.pop()) in [2, 3] and dice_numbers.count(set_dice_numbers.pop()) in [2, 3]:
                            temp_points[i] = 25

                # MINI SERIE
                if i == 11:
                    counted = 1
                    sorted_dice_numbers = sorted(dice_numbers)
                    for j in range(len(dice_numbers) - 1):
                        if sorted_dice_numbers[j] + 1 == sorted_dice_numbers[j+1]:
                            counted += 1
                        if counted == 4:
                            temp_points[i] = 30

                # MAXI SERIE
                if i == 12:
                    counted = 1
                    sorted_dice_numbers = sorted(dice_numbers)
                    for j in range(len(dice_numbers) - 1):
                        if sorted_dice_numbers[j] + 1 == sorted_dice_numbers[j+1]:
                            counted += 1
                        if counted == 5:
                            temp_points[i] = 40
                # KNIFFEL
                if i == 13:
                    if len(set(dice_numbers)) == 1:
                        temp_points[i] = 50

                # CHANCE
                if i == 14:
                    temp_points[i] = sum(dice_numbers)
            else:
                temp_points[i] = None
                player_blocked_points[i] = True

        # update table and show points player got and points from roll
        player_texts = self.texts_players_points[player_move-1]
        player_texts_pos = self.texts_points_pos[player_move-1]

        for i in range(len(player_texts)):
            if player_texts_pos[i].inflate(20, 20).collidepoint(mouse_pos):
                if i not in self.UNCLICKABLE_POINTS and not player_blocked_points[i]:
                    player_texts[i] = self.font.render(str(temp_points[i]), 1, GREEN)
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            player_blocked_points[i] = True
                            player_texts[i] = self.font.render(str(temp_points[i]), 1, RED)
                            player_points[i] = temp_points[i]
                            for j in range(len(player_texts)): # when player ends round make gray his column and give player_points for unblocked rows
                                # update SUMS and BONUS and TOTAL
                                # BONUS
                                if j == 6:
                                    if sum(player_points[:6]) >= 63:
                                        player_points[6] = 35
                                if j == 7:
                                    player_points[7] = sum(player_points[:7])
                                if j == 15:
                                    player_points[15] = sum(player_points[8:15])
                                if j == 16:
                                    player_points[16] = player_points[7] + player_points[15]

                                if not player_blocked_points[j] or j in self.UNCLICKABLE_POINTS:
                                    player_texts[j] = self.font.render(str(player_points[j]), 1, GREY)
                                else:
                                    player_texts[j] = self.font.render(str(player_points[j]), 1, RED)

                            return True
            elif not player_blocked_points[i]:
                player_texts[i] = self.font.render(str(temp_points[i]), 1, BLACK)

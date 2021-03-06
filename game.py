# POKEROWE KOŚCI (inspiracja: https://www.kurnik.pl/kosci/)
import os
import sys
import pygame
from screeninfo import get_monitors
from random import randint
from objects import Die, Dice, Table


pygame.init()

for prop in get_monitors():
    SCREEN_WIDTH = prop.width
    SCREEN_HEIGHT = prop.height

DICE_X = SCREEN_WIDTH*4/5
DICE_Y_SPACE = SCREEN_HEIGHT/8
DICE_PADDING_TOP = SCREEN_HEIGHT/20
GREEN_BG = (48, 128, 72)
DARK_WHITE = (220, 220, 210)
DIE_6_PATH = os.path.join("data", "die_6.png")

# TODO: let block dice
def get_random_dice(DiceGroup, number_of_dice=5):
    if len(DiceGroup) == 0:
        for i in range(number_of_dice):
            DiceGroup.add(Die(randint(1, 6), DICE_X, (i+1)*DICE_Y_SPACE+DICE_PADDING_TOP))
    else:
        new_dice_group = Dice()
        for die in DiceGroup:
            if die.blocked:
                new_dice_group.add(die)
            else:
                new_dice_group.add(Die(randint(1, 6), die.x, die.y))
        DiceGroup.empty()
        for die in new_dice_group:
            DiceGroup.add(die)

pygame.display.set_caption("Dice poker")
pygame.display.set_icon(pygame.image.load(DIE_6_PATH))

screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.RESIZABLE)
players = 2 # changable

dice_group = Dice()
table = Table(screen, DARK_WHITE, SCREEN_WIDTH/4, 10, SCREEN_WIDTH/3, SCREEN_WIDTH/2, players)

shuffle = True
shuffle_times = 0
player_move = 1
get_random_dice(dice_group)
table.draw()

while True:
    mouse_pos = pygame.mouse.get_pos()
    if table.blocked_points[players-1].count(True) == 17: # end of game
        player_total = {}
        totals = []
        won = []
        for i in range(players):
            player_total[i+1] = table.players_points[i][16]
            totals.append(table.players_points[i][16])
        totals = sorted(totals, reverse=True)
        player_total = sorted(player_total.items(), key=lambda x: x[1], reverse=True)
        for i in range(totals.count(totals[0])):
            won.append(player_total[i][0])
        if len(won) == players:
            print("Tie!")
        else:
            print("Won: ", end="")
            [print(player) for player in won]
        break # TODO: info about won
    if table.update(dice_group, player_move, mouse_pos): # clicked
        player_move += 1
        shuffle_times = 0
        dice_group.empty()
        get_random_dice(dice_group)
        if player_move > players:
            player_move = 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # TODO: button to shuffle dice
            changed_state = False
            for die in dice_group:
                if die.rect.collidepoint(mouse_pos):
                    die.change_state()
                    changed_state = True
            if not changed_state and shuffle_times < 2:
                shuffle_times += 1
                get_random_dice(dice_group)

    screen.fill(GREEN_BG)
    dice_group.draw(screen)
    table.draw()
    pygame.display.flip()

# POKEROWE KOŚCI (inspiracja: https://www.kurnik.pl/kosci/)
import os
import sys
import pygame
from random import randint
from objects import Die, Dice


pygame.init()
DICE_X = 1200
DICE_Y_SPACE = 120
GREEN_BG = (48, 128, 72)
DIE_6_PATH = os.path.join("data", "die_6.png")


def get_random_dice(DiceGroup, number_of_dice=5):
    DiceGroup.empty()
    for i in range(number_of_dice):
        DiceGroup.add(Die(randint(1, 6), DICE_X, (i+1)*DICE_Y_SPACE))

screen = pygame.display.set_mode(size=(1900, 1000), flags=pygame.RESIZABLE)
pygame.display.set_caption("Dice poker")
pygame.display.set_icon(pygame.image.load(DIE_6_PATH))
dice_group = Dice()
shuffle = True
get_random_dice(dice_group)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            get_random_dice(dice_group)

    screen.fill(GREEN_BG)
    dice_group.draw(screen)
    pygame.display.flip()
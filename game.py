# POKEROWE KOŚCI (inspiracja: https://www.kurnik.pl/kosci/)
import os
import sys
import pygame
from random import randint
from objects import Die


pygame.init()
DICE_X = 1200
DICE_Y_SPACE = 120
GREEN_BG = (48, 128, 72)
DIE_6_PATH = os.path.join("data", "die_6.png")


def get_random_dice(number=5):
    random_dice = []
    for i in range(number):
        random_dice.append(Die(randint(1, 6), DICE_X, (i+1)*DICE_Y_SPACE))
    return random_dice

screen = pygame.display.set_mode(size=(1900, 1000), flags=pygame.RESIZABLE)
pygame.display.set_caption("Dice poker")
pygame.display.set_icon(pygame.image.load(DIE_6_PATH))
shuffle = True
random_dice = get_random_dice()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            random_dice = get_random_dice()

    screen.fill(GREEN_BG)
    for die in random_dice:
        die.draw(screen)
    pygame.display.flip()
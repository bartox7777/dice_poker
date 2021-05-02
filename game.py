# POKEROWE KOŚCI (inspiracja: https://www.kurnik.pl/kosci/)
import os
import sys
import pygame
from random import randint
from objects import Die


pygame.init()
X = 1200
Y_SPACE = 120


def get_random_dice(number=5):
    random_dice = []
    for i in range(number):
        random_dice.append(Die(randint(1, 6), X, (i+1)*Y_SPACE))
    return random_dice

screen = pygame.display.set_mode(size=(1900, 1000), flags=pygame.RESIZABLE)
pygame.display.set_caption("Dice poker")
pygame.display.set_icon(pygame.image.load(os.path.join("data", "die_6.png")))
shuffle = True
random_dice = get_random_dice()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            random_dice = get_random_dice()

    screen.fill((48, 128, 72))
    for die in random_dice:
        die.draw(screen)
    pygame.display.flip()
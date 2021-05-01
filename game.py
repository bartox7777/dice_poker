# POKEROWE KOŚCI (inspiracja: https://www.kurnik.pl/kosci/)
import sys
import pygame
from objects import Dice


pygame.init()

screen = pygame.display.set_mode(size=(1900, 1000), flags=pygame.RESIZABLE)
# dice = pygame.image.load("dice_1.png")
# dice_rect = ball.get_rect()
test_dice = Dice("dice_1.png")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill((48, 128, 72))
    test_dice.draw(screen)
    pygame.display.flip()
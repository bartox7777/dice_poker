import pygame


pygame.init()


class Dice:
    def __init__(self, image_path, x=0, y=0):
        self.dice = pygame.image.load(image_path)
        self.dice_rect = self.dice.get_rect(x=x, y=y)

    def draw(self, screen, x=None, y=None):
        screen.blit(self.dice, self.dice_rect)
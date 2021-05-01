import pygame


pygame.init()


class Dice:
    def __init__(self, dice_number=1, x=0, y=0):
        self.dice_number = dice_number
        if dice_number not in range(1, 7):
            raise Exception("dice_number must be between 1 and 6")
        dice_images = ["dice_{}.png".format(i+1) for i in range(6)]
        self.dice = pygame.image.load(dice_images[dice_number-1])
        self.dice_rect = self.dice.get_rect(x=x, y=y)

    def draw(self, screen, x=None, y=None):
        if x is not None:
            self.dice_rect.x = x
        if y is not None:
            self.dice_rect.y = y
        screen.blit(self.dice, self.dice_rect)

    def __repr__(self):
        return "Dice {}".format(self.dice_number)
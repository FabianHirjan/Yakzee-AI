from dice import Dice
from button import Button
import pygame

WHITE = (255, 255, 255)


class Game:
    def __init__(self):
        self.dices = [Dice((150 + i * 100, 450)) for i in range(5)]
        self.roll_button = Button("Roll Dice", (325, 550), (120, 50))

    def roll_dices(self):
        for dice in self.dices:
            dice.roll()

    def draw(self, screen):
        screen.fill(WHITE)
        for dice in self.dices:
            dice.draw(screen)
        self.roll_button.draw(screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.roll_button.is_clicked(event.pos):
            self.roll_dices()
            print([dice.value for dice in self.dices])

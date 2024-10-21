import pygame
import random

BLACK = (0, 0, 0)


class Dice:
    def __init__(self, position):
        self.value = 1
        self.position = position
        self.size = 50

    def roll(self):
        self.value = random.randint(1, 6)

    def draw(self, screen):
        pygame.draw.rect(
            screen, BLACK, (self.position[0], self.position[1], self.size, self.size), 2)
        self.draw_text(screen)

    def draw_text(self, screen):
        font = pygame.font.Font(None, 36)
        text_surface = font.render(str(self.value), True, BLACK)
        screen.blit(
            text_surface, (self.position[0] + 15, self.position[1] + 10))

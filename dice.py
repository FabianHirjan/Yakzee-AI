import pygame
import random

BLACK = (0, 0, 0)


class Dice:
    def __init__(self, position):
        self.value = 1
        self.position = position
        self.size = 50
        self.isKept = False
        # Definirea rect-ului
        self.rect = pygame.Rect(position[0], position[1], self.size, self.size)

    def roll(self):
        if not self.isKept:
            self.value = random.randint(1, 6)

    def draw(self, screen):
        color = (0, 255, 0) if self.isKept else (
            255, 0, 0)  # Culoare în funcție de starea isKept
        # Folosește self.rect pentru desenare
        pygame.draw.rect(screen, color, self.rect, 2)
        self.draw_text(screen)

    def draw_text(self, screen):
        font = pygame.font.Font(None, 36)
        text_surface = font.render(str(self.value), True, BLACK)
        screen.blit(
            text_surface, (self.position[0] + 15, self.position[1] + 10))

    def keep(self):
        if self.value != 0:
            self.isKept = True

    def unkeep(self):
        self.isKept = False

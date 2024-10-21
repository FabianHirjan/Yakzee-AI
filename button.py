import pygame

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)


class Button:
    def __init__(self, text, position, size):
        self.text = text
        self.rect = pygame.Rect(position, size)

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.rect)
        self.draw_text(screen)

    def draw_text(self, screen):
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, WHITE)
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class UIElement:
    def __init__(self, text, position, font, color):
        self.text = text
        self.position = position
        self.font = font
        self.color = color
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect(topleft=self.position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Label(UIElement):
    def __init__(self, text, position, font, color):
        super().__init__(text, position, font, color)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class Button(UIElement):
    def __init__(self, text, position, font, color, action=None):
        super().__init__(text, position, font, color)
        self.action = action

    def click(self):
        if self.action:
            self.action()

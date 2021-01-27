import pygame
from constants import COLOR_INACTIVE, COLOR_ACTIVE


class InputBox:
    def __init__(self, game, x, y, w, h, text=''):
        pygame.font.init()
        self.game = game
        self.FONT = pygame.font.Font(None, 30)
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = self.FONT.render(text, True, self.color)
        self.active = False
        self.first_time = 0

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the box rect
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
                self.first_time += 1
                self.color = COLOR_ACTIVE
                self.text = '' if not self.first_time > 1 else self.text
                self.txt_surface = self.FONT.render(self.text, True, self.color)
            else:
                self.color = COLOR_INACTIVE
                self.txt_surface = self.FONT.render(self.text, True, self.color)
                self.active = False

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.FONT.render(self.text, True, self.color)
                self.process_logic()

    def process_logic(self):
        if max(190, self.txt_surface.get_width()) != 190:
            self.active = False

    def process_draw(self):
        self.game.screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(self.game.screen, self.color, self.rect, 2)

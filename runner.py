import pygame
import sys

BLACK = (0, 0, 0)
GREY = (128, 128, 128)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
pygame.init()


screen = pygame.display.set_mode((1020, 680))
pygame.display.set_caption('Pygame Window Test')

pygame.key.set_repeat(300, 30)

class TextInput:
    def __init__(self, rect, font, color):
        self.rect = rect
        self.color = color
        self.font = font
        self.text = ''
        self.focused = False

    def handle_event(self, event):
        if self.focused:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print(f'Text entered in box ({self.rect}): {self.text}')
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw(self, surface):
        box_color = self.color if not self.focused else GREEN
        pygame.draw.rect(surface, box_color, self.rect, 2)
        text_surface = self.font.render(self.text, True, WHITE)
        surface.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

    def handle_click(self, pos):
        # Check if the click is within the text box
        if self.rect.collidepoint(pos):
            self.focused = True
        else:
            self.focused = False

input_text = ''

def draw_button(x, y, width, height, color, text):
    pygame.draw.rect(screen, color, (x, y, width, height))
    font = pygame.font.Font(None, 24)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_surface, text_rect)

input_box1 = TextInput(pygame.Rect(50, 50, 300, 40), pygame.font.Font(None, 24), GREY)
input_box2 = TextInput(pygame.Rect(500, 50, 300, 40), pygame.font.Font(None, 24), GREY)

input_boxes = [input_box1, input_box2]

running = True
while running:
    screen.fill(BLACK)

    for box in input_boxes:
        box.draw(screen)

    draw_button(150, 100, 100, 50, GREY, 'Start')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if 150 <= mouse_pos[0] <= 250 and 100 <= mouse_pos[1] <= 150:
                print(input_boxes[1].text)
            for box in input_boxes:
                box.handle_click(mouse_pos)
        for box in input_boxes:
            box.handle_event(event)

    pygame.display.flip()


pygame.quit()
sys.exit()
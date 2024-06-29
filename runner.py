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
    def __init__(self, rect, font, color, placeholder):
        self.rect = rect
        self.color = color
        self.font = font
        self.text = ''
        self.focused = False
        self.placeholder = placeholder

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
        display_text = self.text if self.text or self.focused else self.placeholder
        text_color = WHITE if self.text or self.focused else GREY
        pygame.draw.rect(surface, box_color, self.rect, 2)
        text_surface = self.font.render(display_text, True, text_color)
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
    font = pygame.font.Font(None, 32)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_surface, text_rect)

def draw_button_with_plus(surface, rect, color, plus_color):
    pygame.draw.rect(surface, color, rect)
    plus_thickness = 5
    # Horizontal line of the plus sign
    pygame.draw.line(surface, plus_color, (rect.x + 30, rect.centery), (rect.right - 30, rect.centery), plus_thickness)
    # Vertical line of the plus sign
    pygame.draw.line(surface, plus_color, (rect.centerx, rect.y + 30), (rect.centerx, rect.bottom - 30), plus_thickness)


X_OFFSET = 280
Y_OFFSET = 70

input_box1 = TextInput(pygame.Rect(80, 50, 250, 40), pygame.font.Font(None, 24), GREY, " MIN  RATE")
input_box2 = TextInput(pygame.Rect(360, 50, 250, 40), pygame.font.Font(None, 24), GREY, " MAX  WEIGHT")
input_box3 = TextInput(pygame.Rect(640, 50, 250, 40), pygame.font.Font(None, 24), GREY, " Origin")
input_box4 = TextInput(pygame.Rect(80, 120, 250, 40), pygame.font.Font(None, 24), GREY, " Destination")

input_boxes = [input_box1, input_box2, input_box3, input_box4]

running = True

more_buttonX = 475
more_buttonY = 120

mb_clicks = 1

dest_boxes = 1

mb_color = GREEN

while running:
    screen.fill(BLACK)

    for box in input_boxes:
        box.draw(screen)

    # Start Button
    draw_button(700, 580, 250, 50, GREY, 'Start')

    # Button to add more input boxes
    button_rect = pygame.Rect(more_buttonX, more_buttonY, 40, 40)
    draw_button_with_plus(screen, button_rect, GREY, mb_color)

    # Button to remove last input box
    draw_button(80, 580, 160, 50, GREY, 'Remove Input')



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if 700 <= mouse_pos[0] <= 950 and 580 <= mouse_pos[1] <= 630:
                print(input_boxes[1].text)
            elif more_buttonX <= mouse_pos[0] <= more_buttonX + 40 and more_buttonY <= mouse_pos[1] <= more_buttonY + 40:
                if dest_boxes == 15:
                    continue
                elif dest_boxes == 14:
                    mb_color = RED

                mb_clicks += 1
                dest_boxes += 1

                new_input = TextInput(pygame.Rect(more_buttonX - 115, more_buttonY, 250, 40), pygame.font.Font(None, 24), GREY, " Destination")
                input_boxes.append(new_input)

                if mb_clicks >= 3:
                    mb_clicks = 0
                    more_buttonX -= X_OFFSET * 2
                    more_buttonY += Y_OFFSET

                else:
                    more_buttonX += X_OFFSET
            elif 80 <= mouse_pos[0] <= 240 and 580 <= mouse_pos[1] <= 630:
                if dest_boxes == 1:
                    continue
                else:
                    if dest_boxes == 15:
                        mb_color = GREEN
                    dest_boxes -= 1
                    input_boxes.pop()

                    if 0 < mb_clicks <= 3:
                        mb_clicks -= 1
                        more_buttonX -= X_OFFSET

                    else:
                        mb_clicks = 2
                        more_buttonX += X_OFFSET * 2
                        more_buttonY -= Y_OFFSET


            for box in input_boxes:
                box.handle_click(mouse_pos)
        for box in input_boxes:
            box.handle_event(event)

    pygame.display.flip()


pygame.quit()
sys.exit()
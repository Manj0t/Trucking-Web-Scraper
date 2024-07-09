import pygame
import sys
import subprocess
import json

# Define colors
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((1020, 680))
pygame.display.set_caption('Pygame Window Test')

# Set keyboard repeat delay
pygame.key.set_repeat(300, 30)

class TextInput:
    """
    Initialize the TextInput object.

    Parameters:
    rect (pygame.Rect): Rectangle defining the position and size of the input box.
    font (pygame.font.Font): Font used for rendering text.
    color (tuple): Color of the input box.
    placeholder (str): Placeholder text displayed when the input box is empty.
    """
    def __init__(self, rect, font, color, placeholder):
        self.rect = rect
        self.color = color
        self.font = font
        self.text = ''
        self.focused = False
        self.placeholder = placeholder

    """
    Handle events related to the TextInput object.

    Parameters:
    event (pygame.event.Event): Event to handle.
    """
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

    """
    Draw the TextInput box on the surface.

    Parameters:
    surface (pygame.Surface): Surface to draw on.
    """
    def draw(self, surface):
        box_color = self.color if not self.focused else GREEN
        display_text = self.text if self.text or self.focused else self.placeholder
        text_color = WHITE if self.text or self.focused else GREY
        pygame.draw.rect(surface, box_color, self.rect, 2)
        text_surface = self.font.render(display_text, True, text_color)
        surface.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

    """
    Handle mouse click events.

    Parameters:
    pos (tuple): Position of the mouse click.
    """
    def handle_click(self, pos):
        # Check if the click is within the text box
        if self.rect.collidepoint(pos):
            self.focused = True
        else:
            self.focused = False

input_text = ''

"""
Draw a button on the screen.

Parameters:
x (int): X-coordinate of the button.
y (int): Y-coordinate of the button.
width (int): Width of the button.
height (int): Height of the button.
color (tuple): Color of the button.
text (str): Text displayed on the button.
"""
def draw_button(x, y, width, height, color, text):
    pygame.draw.rect(screen, color, (x, y, width, height))
    font = pygame.font.Font(None, 32)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_surface, text_rect)

    """
    Draw a button to add more text boxes.

    Parameters:
    surface (pygame.Surface): Surface to draw on.
    rect (pygame.Rect): Rectangle defining the position and size of the button.
    color (tuple): Color of the button.
    plus_color (tuple): Color of the plus sign.
    """
def draw_button_with_plus(surface, rect, color, plus_color):
    pygame.draw.rect(surface, color, rect)
    plus_thickness = 5
    # Horizontal line of the plus sign
    pygame.draw.line(surface, plus_color, (rect.x + 30, rect.centery), (rect.right - 30, rect.centery), plus_thickness)
    # Vertical line of the plus sign
    pygame.draw.line(surface, plus_color, (rect.centerx, rect.y + 30), (rect.centerx, rect.bottom - 30), plus_thickness)

# Offset values for input box positioning
X_OFFSET = 280
Y_OFFSET = 70

# Initialize TextInput objects
input_box1 = TextInput(pygame.Rect(80, 50, 250, 40), pygame.font.Font(None, 24), GREY, " MIN  RATE")
input_box2 = TextInput(pygame.Rect(360, 50, 250, 40), pygame.font.Font(None, 24), GREY, " MAX  WEIGHT")
input_box3 = TextInput(pygame.Rect(640, 50, 250, 40), pygame.font.Font(None, 24), GREY, " Origin")
input_box4 = TextInput(pygame.Rect(80, 120, 250, 40), pygame.font.Font(None, 24), GREY, " Start Date  Ex. 07/02/2024")
input_box5 = TextInput(pygame.Rect(360, 120, 250, 40), pygame.font.Font(None, 24), GREY, " End Date  Ex. 07/02/2024")
input_box6 = TextInput(pygame.Rect(640, 120, 250, 40), pygame.font.Font(None, 24), GREY, " Destination")

input_boxes = [input_box1, input_box2, input_box3, input_box4, input_box5, input_box6]

# Initialize running state and button positions
running = True

# This button will create more text boxes
more_buttonX = 195
more_buttonY = 190

# Tracks how many times the more text box button is clicked
mb_clicks = 0
# Tracks how many destination boxes there are
dest_boxes = 1

mb_color = GREEN

data = []

# Determines wether or not to run the primary scraping program
start_program = False

start_end_text = 'Start'
start_end_color = GREY

process = None

# Main loop
while running:
    screen.fill(BLACK)

    for box in input_boxes:
        box.draw(screen)

    # Start Button
    draw_button(700, 580, 250, 50, start_end_color, start_end_text)

    # Button to add more input boxes
    button_rect = pygame.Rect(more_buttonX, more_buttonY, 40, 40)
    draw_button_with_plus(screen, button_rect, GREY, mb_color)

    # Button to remove last input box
    draw_button(80, 580, 160, 50, GREY, 'Remove Input')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # if the program exits, make sure to exit scraping program if it is still running
            if process:
                process.terminate()
                process = None
            running = False

        # Start the scraping program if start is clicked
        # This will change the start button to a stop button to stop the scraping program
        if start_program and start_end_text == 'Start':
            data_json = json.dumps(data)
            # Run main script and pass the JSON string as an argument
            python_executable = "C:/Users/fitem/AppData/Roaming/JetBrains/PyCharm2024.1/Trucking/venv/Scripts/python.exe"
            process = subprocess.Popen([python_executable, 'main.py', data_json])

            start_end_text = 'Stop Program'
            start_end_color = RED

            data.clear()
            start_program = False

        # Stops the program if the button is in Stop Program mode
        elif start_program and start_end_text == 'Stop Program':
            if process:
                process.terminate()
                process = None

            start_end_text = 'Start'
            start_end_color = GREY

            data.clear()
            start_program = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Checks if the start button has been clicked
            if 700 <= mouse_pos[0] <= 950 and 580 <= mouse_pos[1] <= 630:
                # Adds the inputed text to a data list to be passed into scraping program
                for input_box in input_boxes:
                    data.append(input_box.text)
                start_program = True
            # Checks if the button to add more destination input boxes has been clicked
            elif more_buttonX <= mouse_pos[0] <= more_buttonX + 40 and more_buttonY <= mouse_pos[1] <= more_buttonY + 40:
                # Checks if max number of destinatino boxes has already been created
                if dest_boxes == 13:
                    continue
                elif dest_boxes == 12:
                    mb_color = RED

                mb_clicks += 1
                dest_boxes += 1

                new_input = TextInput(pygame.Rect(more_buttonX - 115, more_buttonY, 250, 40), pygame.font.Font(None, 24), GREY, " Destination")
                input_boxes.append(new_input)

                # Logic to move to next row if there are 3 destination boxes on a row
                if mb_clicks >= 3:
                    mb_clicks = 0
                    more_buttonX -= X_OFFSET * 2
                    more_buttonY += Y_OFFSET

                else:
                    more_buttonX += X_OFFSET
            # Checks if the remove destination box button has been clicked
            elif 80 <= mouse_pos[0] <= 240 and 580 <= mouse_pos[1] <= 630:
                if dest_boxes == 1:
                    continue
                else:
                    if dest_boxes == 13:
                        mb_color = GREEN
                    dest_boxes -= 1
                    input_boxes.pop()

                    # Logic for moving up a row if there are not 3 destination boxes on the row above
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
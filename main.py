import pygame
import sys
import os
from typing import List, Tuple

# Initialize pygame
pygame.init()

# Get screen dimensions and set up screen accordingly
info = pygame.display.Info() 
screen_width, screen_height = info.current_w, info.current_h
# screen = pygame.display.set_mode((screen_width, screen_height))

# Set window title and icon
# pygame.display.set_caption("")
# favicon = pygame.image.load("")
# pygame.display.set_icon(favicon)

# Screen dimensions
SCREEN_WIDTH = screen_width
SCREEN_HEIGHT = screen_height

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)
GREEN = (50, 205, 50)
RED = (220, 20, 60)
YELLOW = (255, 255, 0)

# Fonts
FONT_LARGE = pygame.font.SysFont('Arial', 36)
FONT_MEDIUM = pygame.font.SysFont('Arial', 28)
FONT_SMALL = pygame.font.SysFont('Arial', 20)

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str, 
                 color: Tuple[int, int, int] = LIGHT_BLUE, 
                 hover_color: Tuple[int, int, int] = DARK_BLUE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.text_surface = FONT_MEDIUM.render(text, True, BLACK)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        
    def draw(self, screen: pygame.Surface):
        # Draw button
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=10)  # Border
        
        # Draw text
        screen.blit(self.text_surface, self.text_rect)
    
    def check_hover(self, mouse_pos: Tuple[int, int]):
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
            return True
        else:
            self.current_color = self.color
            return False
    
    def is_clicked(self, mouse_pos: Tuple[int, int], mouse_clicked: bool):
        return self.check_hover(mouse_pos) and mouse_clicked


class TextInput:
    def __init__(self, x, y, width, height, font=FONT_SMALL, color=WHITE, border_color=BLACK):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.border_color = border_color
        self.text = ""
        self.font = font
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active state if clicked
            self.active = self.rect.collidepoint(event.pos)
        if self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def draw(self, screen):
        # Draw box
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 2)
        # Draw text
        txt_surface = self.font.render(self.text, True, BLACK)
        screen.blit(txt_surface, (self.rect.x+5, self.rect.y+8))

    def get_text(self):
        return self.text


class Flashcard:
    def __init__(self, question: str, options: List[str], correct_answer: int):
        self.question = question
        self.options = options
        self.correct_answer = correct_answer  # Index of the correct option


class FlashcardApp:
    def __init__(self):
        # Initialize screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flashcard App")
        
        # Game states
        self.HOME = 0
        self.CARDS = 1
        self.current_state = self.HOME
        
        # Home screen elements
        self.home_buttons = [
            Button(SCREEN_WIDTH//2 - 150, 200, 300, 60, "Start Flashcards"),
            Button(SCREEN_WIDTH//2 - 150, 300, 300, 60, "Settings"),
            Button(SCREEN_WIDTH//2 - 150, 400, 300, 60, "Exit")
        ]
        
        # Card screen elements
        self.next_button = Button(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 70, 120, 50, "Next")
        self.back_button = Button(30, SCREEN_HEIGHT - 70, 120, 50, "Back")
        
        # Flashcard data (sample cards)
        self.flashcards = [
            Flashcard("What is the capital of France?", 
                     ["Berlin", "London", "Paris", "Madrid"], 2),
            Flashcard("Which planet is known as the Red Planet?", 
                     ["Venus", "Mars", "Jupiter", "Saturn"], 1),
            Flashcard("What is 7 x 8?", 
                     ["54", "56", "64", "72"], 1)
        ]
        
        self.current_card_index = 0
        self.selected_option = None
        self.answer_submitted = False
        
    def run(self):
        running = True
        clock = pygame.time.Clock()
        
        while running:
            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = False
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_clicked = True
            
            # Clear screen
            self.screen.fill(WHITE)
            
            # Update and render based on current state
            if self.current_state == self.HOME:
                self.handle_home_screen(mouse_pos, mouse_clicked)
            elif self.current_state == self.CARDS:
                self.handle_cards_screen(mouse_pos, mouse_clicked)
            
            # Update display
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()
    
    def handle_home_screen(self, mouse_pos: Tuple[int, int], mouse_clicked: bool):
        # Draw title
        title_text = FONT_LARGE.render("Flashcard App", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Draw and check buttons
        for button in self.home_buttons:
            button.draw(self.screen)
            if button.is_clicked(mouse_pos, mouse_clicked):
                if button.text == "Start Flashcards":
                    self.current_state = self.CARDS
                    self.current_card_index = 0
                    self.selected_option = None
                    self.answer_submitted = False
                elif button.text == "Exit":
                    pygame.quit()
                    sys.exit()
                # Settings button functionality can be added later
    
    def handle_cards_screen(self, mouse_pos: Tuple[int, int], mouse_clicked: bool):
        current_card = self.flashcards[self.current_card_index]
        
        # Draw question
        question_text = FONT_MEDIUM.render(current_card.question, True, BLACK)
        question_rect = question_text.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(question_text, question_rect)
        
        # Draw options
        option_buttons = []
        for i, option in enumerate(current_card.options):
            # Calculate position (2x2 grid)
            col = i % 2
            row = i // 2
            x = SCREEN_WIDTH//4 + (col * SCREEN_WIDTH//2) - 120
            y = 200 + (row * 100)
            
            # Determine color based on answer status
            if self.answer_submitted:
                if i == current_card.correct_answer:
                    color = GREEN  # Correct answer is green
                elif i == self.selected_option and i != current_card.correct_answer:
                    color = RED    # Incorrect selected answer is red
                else:
                    color = LIGHT_BLUE
            else:
                color = LIGHT_BLUE if i != self.selected_option else YELLOW
            
            button = Button(x, y, 240, 60, option, color)
            button.draw(self.screen)
            option_buttons.append(button)
            
            # Check if option is clicked
            if not self.answer_submitted and button.is_clicked(mouse_pos, mouse_clicked):
                self.selected_option = i
        
        # Draw navigation buttons
        self.back_button.draw(self.screen)
        if self.back_button.is_clicked(mouse_pos, mouse_clicked):
            self.current_state = self.HOME
        
        self.next_button.draw(self.screen)
        if self.next_button.is_clicked(mouse_pos, mouse_clicked):
            if self.answer_submitted:
                # Move to next card
                self.current_card_index = (self.current_card_index + 1) % len(self.flashcards)
                self.selected_option = None
                self.answer_submitted = False
            elif self.selected_option is not None:
                # Submit answer
                self.answer_submitted = True
        
        # Draw card indicator
        card_indicator = f"Card {self.current_card_index + 1} of {len(self.flashcards)}"
        indicator_text = FONT_SMALL.render(card_indicator, True, BLACK)
        self.screen.blit(indicator_text, (SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT - 60))
        
        # Button state text
        if not self.answer_submitted and self.selected_option is not None:
            submit_text = FONT_SMALL.render("Click Next to submit", True, BLACK)
            self.screen.blit(submit_text, (SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT - 90))
        elif self.answer_submitted:
            next_text = FONT_SMALL.render("Click Next for next card", True, BLACK)
            self.screen.blit(next_text, (SCREEN_WIDTH//2 - 90, SCREEN_HEIGHT - 90))


if __name__ == "__main__":
    app = FlashcardApp()
    app.run()

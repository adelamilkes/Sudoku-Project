import pygame
import sys
from board import Board

# Initialize PyGame
pygame.init()

# Constants for the game screen
SCREEN_WIDTH = 540
SCREEN_HEIGHT = 600  # Increased height to allow space for buttons
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255,255, 0)

# Font for rendering text
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)
big_font = pygame.font.Font(None, 60)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sudoku Game")

# Function to draw the game start screen
def draw_start_screen():
    screen.fill(WHITE)
    button_width = 200
    button_height = 50
    button_border_thickness = 2
    button_border_color = BLACK

    easy_button_rect = pygame.Rect(170, 200, button_width, button_height)
    pygame.draw.rect(screen, GREEN, easy_button_rect)
    pygame.draw.rect(screen, button_border_color, easy_button_rect, button_border_thickness)

    medium_button_rect = pygame.Rect(170, 280, button_width, button_height)
    pygame.draw.rect(screen, YELLOW, medium_button_rect)
    pygame.draw.rect(screen, button_border_color, medium_button_rect, button_border_thickness)

    hard_button_rect = pygame.Rect(170, 360, button_width, button_height)
    pygame.draw.rect(screen, RED, hard_button_rect)
    pygame.draw.rect(screen, button_border_color, hard_button_rect, button_border_thickness)

    start_text = big_font.render("Sudoku", True, BLACK)
    easy_text = font.render("Easy", True, BLACK)
    medium_text = font.render("Medium", True, BLACK)
    hard_text = font.render("Hard", True, BLACK)

    screen.blit(start_text, (190, 115))
    screen.blit(easy_text, (230, 215))
    screen.blit(medium_text, (230, 295))
    screen.blit(hard_text, (230, 375))

    pygame.display.flip()

# Function to draw game-in-progress screen
def draw_game_in_progress(board, reset_button, restart_button, exit_button):
    screen.fill(WHITE)
    board.draw()  # Draw the Sudoku board

    # Draw the control buttons
    pygame.draw.rect(screen, (200, 200, 200), reset_button)
    pygame.draw.rect(screen, (200, 200, 200), restart_button)
    pygame.draw.rect(screen, (200, 200, 200), exit_button)

    reset_text = small_font.render("Reset", True, BLACK)
    restart_text = small_font.render("Restart", True, BLACK)
    exit_text = small_font.render("Exit", True, BLACK)

    screen.blit(reset_text, (190,560))
    screen.blit(restart_text, (270, 560))
    screen.blit(exit_text, (375, 560))

    pygame.display.flip()

# Function to draw the success screen with an exit button
def draw_success_screen(exit_button):
    screen.fill(WHITE)
    text = font.render("Game Won!", True, GREEN)
    screen.blit(text, (200, 200))

    pygame.draw.rect(screen, (200, 200, 200), exit_button)
    exit_text = font.render("Exit", True, BLACK)
    screen.blit(exit_text, (250, 330))

    pygame.display.flip()

# Function to draw the failure screen with a restart button
def draw_failure_screen(restart_button):
    screen.fill(WHITE)
    text = font.render("Game Over:(", True, RED)
    screen.blit(text, (200, 200))

    pygame.draw.rect(screen, (200, 200, 200), restart_button)
    restart_text = font.render("Restart", True, BLACK)
    screen.blit(restart_text, (240, 330))

    pygame.display.flip()

# Main game loop
def main():
    # Initialize the game state
    game_state = "start"
    sudoku_board = None
    difficulty = None
    clock = pygame.time.Clock()

    # Control button definitions for the game-in-progress screen
    reset_button = pygame.Rect(170, 550, 80, 40)
    restart_button = pygame.Rect(260, 550, 80, 40)
    exit_button = pygame.Rect(350, 550, 80, 40)

    # Additional control buttons for success and failure screens
    failure_restart_button = pygame.Rect(230, 320, 100, 40)
    success_exit_button = pygame.Rect(230, 320, 80, 40)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle transitions between game states
            if game_state == "start":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if 170 <= x <= 370:
                        if 200 <= y <= 250:
                            difficulty = "easy"
                            game_state = "in_game"
                            sudoku_board = Board(SCREEN_WIDTH, SCREEN_HEIGHT - 60, screen, difficulty)
                        elif 280 <= y <= 330:
                            difficulty = "medium"
                            game_state = "in_game"
                            sudoku_board = Board(SCREEN_WIDTH, SCREEN_HEIGHT - 60, screen, difficulty)
                        elif 360 <= 410:
                            difficulty = "hard"
                            game_state = "in_game"
                            sudoku_board = Board(SCREEN_WIDTH, SCREEN_HEIGHT - 60, screen, difficulty)

            elif game_state == "in_game":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_result = sudoku_board.click(*event.pos)
                    if click_result:
                        row, col = click_result
                        sudoku_board.select(row, col)

                    if reset_button.collidepoint(event.pos):
                        sudoku_board.reset_to_original()

                    elif restart_button.collidepoint(event.pos):
                        game_state = "start"

                    elif exit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

                if event.type == pygame.KEYDOWN:
                    if sudoku_board.selected:

                        current_row, current_col = sudoku_board.selected.row, sudoku_board.selected.col

                        if event.key == pygame.K_UP:
                            current_row = max(0, current_row - 1)

                        elif event.key == pygame.K_DOWN:
                            current_row = min(8, current_row + 1)  # Adjust to maximum row index (0-8)

                        elif event.key == pygame.K_LEFT:
                            current_col = max(0, current_col - 1)

                        elif event.key == pygame.K_RIGHT:
                            current_col = min(8, current_col + 1)  # Adjust to maximum column index (0-8)

                        sudoku_board.select(current_row, current_col)

                        if pygame.K_0 <= event.key <= pygame.K_9:
                            value = event.key - pygame.K_0
                            if value > 0:
                                sudoku_board.sketch(value)
                        elif event.key == pygame.K_RETURN:
                            sudoku_board.place_number(sudoku_board.selected.sketched_value)

            if game_state == "in_game":
                draw_game_in_progress(sudoku_board, reset_button, restart_button, exit_button)

                if sudoku_board.is_full():
                    sudoku_board.update_board()
                    if sudoku_board.check_board():
                        game_state = "success"
                    else:
                        game_state = "failure"

            elif game_state == "success":
                draw_success_screen(success_exit_button)
                if event.type == pygame.MOUSEBUTTONDOWN and success_exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

            elif game_state == "failure":
                draw_failure_screen(failure_restart_button)
                if event.type == pygame.MOUSEBUTTONDOWN and failure_restart_button.collidepoint(event.pos):
                    game_state = "start"

            elif game_state == "start":
                draw_start_screen()

        clock.tick(FPS)

# Entry point for the script
if __name__ == "__main__":
    main()
import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 600, 600
ROWS, COLS = 5, 5
SQUARE_SIZE = WIDTH // COLS
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]  

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Fill Puzzle")

board = [[-1 for _ in range(COLS)] for _ in range(ROWS)]
selected_square = None

def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            color = (200, 200, 200) if board[row][col] == -1 else COLORS[board[row][col]]
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(screen, (0, 0, 0), (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)

def get_adjacent_colors(row, col):
    """Returns a set of colors of all adjacent squares (including diagonals)."""
    adjacent_colors = set()
    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),   
        (-1, -1), (-1, 1), (1, -1), (1, 1)  
    ]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] != -1:
            adjacent_colors.add(board[r][c])
    return adjacent_colors

def get_available_colors(row, col):
    """Determines available colors for the clicked square based on adjacent squares."""
    adjacent_colors = get_adjacent_colors(row, col)
    return [i for i, color in enumerate(COLORS) if i not in adjacent_colors]

def handle_click(pos):
    """Handles a click event to cycle through available colors in the clicked square."""
    global selected_square

    col, row = pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE

    available_colors = get_available_colors(row, col)

    if board[row][col] == -1 and available_colors:
        board[row][col] = available_colors[0]
    elif available_colors:
        current_color = board[row][col]
        next_color_index = (available_colors.index(current_color) + 1) % len(available_colors) if current_color in available_colors else 0
        board[row][col] = available_colors[next_color_index]

def check_win_condition():
    """Checks if all squares are filled without color conflicts."""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == -1 or board[row][col] in get_adjacent_colors(row, col):
                return False
    return True

def main():
    clock = pygame.time.Clock()
    game_over = False
    
    while True:
        screen.fill((255, 255, 255))
        draw_grid()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                handle_click(pygame.mouse.get_pos())
                if check_win_condition():
                    game_over = True

        if game_over:
            font = pygame.font.SysFont(None, 60)
            text = font.render("You Win!", True, (0, 128, 0))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()

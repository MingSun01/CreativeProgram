import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 600, 400
screen = pygame.display.set_mode((width, height))

# Fonts
font = pygame.font.SysFont(None, 36)
large_font = pygame.font.SysFont(None, 72)

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
gray = (200, 200, 200)

# Game variables
dot_x, dot_y = 50, height - 40
dot_radius = 10
jump = False
jump_height = 10
gravity = 1
obstacles = []
obstacle_width = 20
obstacle_height = 40
speed = 5
score = 0
game_over = False

# Create a clock object to control the game speed
clock = pygame.time.Clock()

# Function to create obstacles
def create_obstacle():
    return [random.randint(width, width + 100), height - obstacle_height]

# Function to update game state
def update_game(dot_y, jump, obstacles, score, jump_height):
    if jump:
        dot_y -= jump_height
        jump_height -= gravity
        if jump_height < -10:
            jump = False
            jump_height = 10
    else:
        if dot_y < height - 40:
            dot_y += gravity
    
    # Move obstacles
    new_obstacles = []
    for obs in obstacles:
        obs[0] -= speed
        if obs[0] > 0:
            new_obstacles.append(obs)
        else:
            score += 1
    
    if len(new_obstacles) == 0 or new_obstacles[-1][0] < width - 200:
        new_obstacles.append(create_obstacle())
    
    return dot_y, jump, new_obstacles, score, jump_height

# Function to check collision
def check_collision(dot_y, obstacles):
    for obs in obstacles:
        if obs[0] < dot_x + dot_radius and obs[0] + obstacle_width > dot_x:
            if dot_y + dot_radius > height - obstacle_height:
                return True
    return False

# Function to draw the score in the top-right corner
def draw_score(score):
    score_text = font.render(f"Score: {score}", True, black)
    screen.blit(score_text, (width - 150, 10))

# Function to display Game Over screen
def display_game_over():
    # "Game Over" text
    game_over_text = large_font.render("Game Over", True, black)
    screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - 100))

    # Reset button
    button_rect = pygame.Rect(width // 2 - 50, height // 2 + 50, 100, 40)
    pygame.draw.rect(screen, black, button_rect, 2)  # Button outline
    pygame.draw.rect(screen, white, button_rect.inflate(-4, -4))  # Button fill
    button_text = font.render("Reset", True, black)
    screen.blit(button_text, (button_rect.centerx - button_text.get_width() // 2, button_rect.centery - button_text.get_height() // 2))
    
    return button_rect

# Function to display "Press Space to Jump!" in the top left corner
def display_jump_instructions():
    jump_text = font.render("Press SPACE to Jump!", True, black)
    screen.blit(jump_text, (10, 10))

# Main game loop
while True:
    if not game_over:
        screen.fill(white)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Jump with 'E'
                    if not jump:
                        jump = True

        # Update the game state
        dot_y, jump, obstacles, score, jump_height = update_game(dot_y, jump, obstacles, score, jump_height)

        # Check for collisions
        if check_collision(dot_y, obstacles):
            game_over = True
        
        # Draw the player (black dot)
        pygame.draw.circle(screen, black, (dot_x, dot_y), dot_radius)
        
        # Draw the obstacles (black rectangles)
        for obs in obstacles:
            pygame.draw.rect(screen, black, (obs[0], height - obstacle_height, obstacle_width, obstacle_height))
        
        # Draw the score in the top-right corner
        draw_score(score)

        # Display "Press Space to Jump!" in the top-left corner
        display_jump_instructions()

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(30)

    else:
        screen.fill(white)

        # Display Game Over screen
        button_rect = display_game_over()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    # Reset the game
                    game_over = False
                    dot_y = height - 40
                    obstacles = []
                    score = 0
                    jump = False

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(30)
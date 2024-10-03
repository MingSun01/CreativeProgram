import streamlit as st
import pygame
import random
import numpy as np

# Initialize pygame
pygame.init()

# Screen dimensions
width, height = 600, 400
screen = pygame.Surface((width, height))

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

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

# Use session state to prevent game from restarting on key press
if 'game_running' not in st.session_state:
    st.session_state.game_running = False

# Streamlit layout
st.title("Simple Dino Run with Dots")

if not st.session_state.game_running:
    start_button = st.button("Start Game")
else:
    start_button = None

# Streamlit placeholder for the canvas
canvas_placeholder = st.empty()

def create_obstacle():
    """Creates a new obstacle at a random location."""
    return [random.randint(width, width + 100), height - obstacle_height]

def update_game(dot_y, jump, obstacles, score):
    """Handles game logic like jumping and moving obstacles."""
    global jump_height  # Make jump_height a global variable

    # Handle jumping
    if jump:
        dot_y -= jump_height
        jump_height -= gravity
        if jump_height < 0:  # When jump is finished
            jump = False
            jump_height = 10  # Reset jump height after jump completes
    else:
        # Bring the dot back down when not jumping
        if dot_y < height - 40:  # Stop falling at ground level
            dot_y += gravity
    
    # Move obstacles and remove them if they go off screen
    new_obstacles = []
    for obs in obstacles:
        obs[0] -= speed
        if obs[0] > 0:
            new_obstacles.append(obs)
        else:
            score += 1
    
    if len(new_obstacles) == 0 or new_obstacles[-1][0] < width - 200:
        new_obstacles.append(create_obstacle())
    
    return dot_y, jump, new_obstacles, score

def check_collision(dot_y, obstacles):
    """Checks if the dot (player) collides with any obstacles."""
    for obs in obstacles:
        if obs[0] < dot_x + dot_radius and obs[0] + obstacle_width > dot_x:
            if dot_y + dot_radius > height - obstacle_height:
                return True
    return False

if start_button and not st.session_state.game_running:
    st.session_state.game_running = True  # Game starts after clicking the button
    st.text("Game Started! Press 'E' to Jump.")
    
    clock = pygame.time.Clock()

    # Reset game state
    dot_y = height - 40
    obstacles = []
    score = 0
    jump = False

    # Main game loop
    while st.session_state.game_running:
        # Check for E key press to make the dot jump
        # for event in pygame.event.get():
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_e:  # Change jump key to 'E'
        #             if not jump:  # Only allow jump if not already jumping
        #                 jump = True
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            if not jump:
                jump = True

        # Update game state
        dot_y, jump, obstacles, score = update_game(dot_y, jump, obstacles, score)

        # Check for collisions
        if check_collision(dot_y, obstacles):
            st.write(f"Game Over! Your Score: {score}")
            st.session_state.game_running = False
            break

        # Clear the screen
        screen.fill(white)

        # Draw the player (black dot)
        pygame.draw.circle(screen, black, (dot_x, dot_y), dot_radius)

        # Draw the obstacles (black rectangles)
        for obs in obstacles:
            pygame.draw.rect(screen, black, (obs[0], height - obstacle_height, obstacle_width, obstacle_height))

        # Convert the pygame surface to an image and display it in the same canvas
        canvas_placeholder.image(pygame.surfarray.array3d(screen).transpose(1, 0, 2), width=width)

        # Control game speed
        clock.tick(30)

# After the game ends, make sure the user can restart with the Start button
if not st.session_state.game_running:
    st.write("Press 'Start Game' to play again.")
import streamlit as st
import pygame
import time
import random

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
obstacles = []
obstacle_width = 20
obstacle_height = 40
speed = 5
score = 0

# Streamlit layout
st.title("Simple Dino Run with Dots")
start_button = st.button("Start Game")

def create_obstacle():
    """Creates a new obstacle at a random location."""
    return [random.randint(width, width + 100), height - obstacle_height]

def update_game(dot_y, jump, obstacles, score, jump_height):
    """Handles game logic like jumping and moving obstacles."""
    # Handle jumping
    if jump:
        dot_y -= jump_height
        jump_height -= 1
        if jump_height < -10:
            jump = False
            jump_height = 10

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
    
    return dot_y, jump, new_obstacles, score, jump_height

def check_collision(dot_y, obstacles):
    """Checks if the dot (player) collides with any obstacles."""
    for obs in obstacles:
        if obs[0] < dot_x + dot_radius and obs[0] + obstacle_width > dot_x:
            if dot_y + dot_radius > height - obstacle_height:
                return True
    return False

if start_button:
    st.text("Game Started! Press 'Space' to Jump.")
    clock = pygame.time.Clock()

    # Main game loop
    while True:
        # Handle user input (jumping)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            jump = True

        # Update game state
        dot_y, jump, obstacles, score, jump_height = update_game(dot_y, jump, obstacles, score, jump_height)

        # Check for collisions
        if check_collision(dot_y, obstacles):
            st.write(f"Game Over! Your Score: {score}")
            break

        # Draw everything
        screen.fill(white)
        pygame.draw.circle(screen, black, (dot_x, dot_y), dot_radius)  # Player
        for obs in obstacles:
            pygame.draw.rect(screen, black, (obs[0], height - obstacle_height, obstacle_width, obstacle_height))  # Obstacles

        # Streamlit rendering
        st.image(pygame.surfarray.array3d(screen).transpose(1, 0, 2), width=width)
        st.write(f"Score: {score}")

        # Control game speed
        clock.tick(30)
import pygame
import asyncio
import random

# Window Constants
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 25  # Size of one grid square

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Snake")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

async def main():
    running = True
    
    # Game Speed
    move_timer = 0
    MOVE_DELAY = 100 # Milliseconds between moves
    
    # Snake Body: A list of Rectangles (Head is at index 0)
    snake = [
        pygame.Rect(100, 100, CELL_SIZE, CELL_SIZE),
        pygame.Rect(75, 100, CELL_SIZE, CELL_SIZE),
        pygame.Rect(50, 100, CELL_SIZE, CELL_SIZE)
    ]
    
    # Direction vector (x, y)
    direction = (1, 0) 
    next_direction = (1, 0) # Prevents 180-degree turns in one frame
    
    food = pygame.Rect(300, 300, CELL_SIZE, CELL_SIZE)
    score = 0

    try:
        font = pygame.font.Font(None, 36)
    except FileNotFoundError:
        font = pygame.font.SysFont("Arial", 36) 
    
    while running:
        dt = clock.tick(60) # Delta time (time since last frame)
        move_timer += dt
        
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, 1):
                    next_direction = (0, -1)
                if event.key == pygame.K_DOWN and direction != (0, -1):
                    next_direction = (0, 1)
                if event.key == pygame.K_LEFT and direction != (1, 0):
                    next_direction = (-1, 0)
                if event.key == pygame.K_RIGHT and direction != (-1, 0):
                    next_direction = (1, 0)

        # 2. Update Game Logic (Movement happens here on a timer)
        if move_timer > MOVE_DELAY:
            move_timer = 0
            
            # Update actual direction
            direction = next_direction

            # 1. Create New Head position calculation
            new_x = snake[0].x + (direction[0] * CELL_SIZE)
            new_y = snake[0].y + (direction[1] * CELL_SIZE)
            
            new_head = pygame.Rect(new_x, new_y, CELL_SIZE, CELL_SIZE)
            
            # === MODIFIED SECTION: Wall Collisions NO LONGER KILL YOU ===
            
            # Check for self-collision (this still kills you)
            if new_head.collidelist(snake) != -1: 
                # Reset Game State
                snake = [
                    pygame.Rect(100, 100, CELL_SIZE, CELL_SIZE),
                    pygame.Rect(75, 100, CELL_SIZE, CELL_SIZE),
                    pygame.Rect(50, 100, CELL_SIZE, CELL_SIZE)
                ]
                direction = (1, 0)
                next_direction = (1, 0)
                score = 0
                MOVE_DELAY = 100 # Reset speed on death
            else:
                # === NEW WRAP-AROUND LOGIC ===
                # If head goes off the edge, move it to the opposite edge
                if new_head.right > WIDTH:
                    new_head.left = 0
                elif new_head.left < 0:
                    new_head.right = WIDTH
                elif new_head.bottom > HEIGHT:
                    new_head.top = 0
                elif new_head.top < 0:
                    new_head.bottom = HEIGHT
                # === END WRAP-AROUND LOGIC ===

                # 2. Add New Head (only if self-collision didn't trigger a reset above)
                snake.insert(0, new_head)
                
                # Check collision with food
                if new_head.colliderect(food):
                    score += 1

                    MOVE_DELAY = max(50, MOVE_DELAY - 2)
                    
                    # Move food to random spot within boundaries
                    food.x = random.randint(0, (WIDTH//CELL_SIZE) - 1) * CELL_SIZE
                    food.y = random.randint(0, (HEIGHT//CELL_SIZE) - 1) * CELL_SIZE
                else:
                    # Only remove tail if we DIDN'T eat
                    snake.pop()
            # ========================================
            
        # 3. Drawing
        screen.fill(BLACK)
        
        # Draw Food
        pygame.draw.rect(screen, RED, food)
        
        # Draw Snake
        for i, part in enumerate(snake):
            if i == 0:
                color = GREEN # Head
            else:
                color = DARK_GREEN # Body
            pygame.draw.rect(screen, color, part)

        # Display the Score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        await asyncio.sleep(0)

# This line ensures the script runs the main function when executed
if __name__ == "__main__":
    asyncio.run(main())

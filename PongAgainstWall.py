import pygame
import random
import Players

# Constants
WIDTH, HEIGHT = 800, 600
BALL_SPEED = 4
PADDLE_SPEED = 7
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class PongEngine:
    def __init__(self):
        pygame.init()
        # Create window
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pong")
        # Ball position & velocity
        self.ball_x = WIDTH // 2
        self.ball_y = WIDTH // 2
        self.ball_dx = random.choice([BALL_SPEED, -BALL_SPEED])
        self.ball_dy = random.choice([BALL_SPEED, -BALL_SPEED])

        # Paddle positions
        self.left_paddle_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.right_paddle_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.score = 0

        self.running = False

    def RunGame(self, player1):
        # Game loop
        self.running = True
        clock = pygame.time.Clock()
        while self.running:
            self.screen.fill(BLACK)
            
            # Update Players
            player1.Update(self.ball_x, self.ball_y, self.ball_dx, self.ball_dy, self.left_paddle_y + PADDLE_HEIGHT/2)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.left_paddle_y += PADDLE_SPEED
                    elif event.key == pygame.K_DOWN:
                        self.left_paddle_y -= PADDLE_SPEED
        
            # Move ball
            self.ball_x += self.ball_dx
            self.ball_y += self.ball_dy
            
            # Ball collision with top/bottom
            if self.ball_y - BALL_RADIUS <= 0 or self.ball_y + BALL_RADIUS >= HEIGHT:
                self.ball_dy *= -1
            
            # Ball collision with paddle
            if (self.ball_x - BALL_RADIUS <= PADDLE_WIDTH and self.left_paddle_y < self.ball_y < self.left_paddle_y + PADDLE_HEIGHT and self.ball_dx < 0):
                self.ball_dx *= -1
                self.score += 1
            
            # Ball collision with wall on right side
            if (self.ball_x + BALL_RADIUS >= WIDTH):
                self.ball_dx *= -1
            
            # Ball out of bounds
            if self.ball_x < 0:
                return self.score   # game ends when bot misses the ball
                self.score = 0
                self.ball_x, self.ball_y = WIDTH // 2, HEIGHT // 2
                self.ball_dx = BALL_SPEED
            
            # Paddle out of bounds
            if(self.left_paddle_y < 0):
                self.left_paddle_y = 0
            if(self.left_paddle_y + PADDLE_HEIGHT > HEIGHT):
                self.left_paddle_y = HEIGHT - PADDLE_HEIGHT

            # Draw paddles and ball
            pygame.draw.rect(self.screen, WHITE, (0, self.left_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
            pygame.draw.circle(self.screen, WHITE, (self.ball_x, self.ball_y), BALL_RADIUS)
            
            # Draw scores
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {self.score}", True, WHITE)
            self.screen.blit(score_text, (WIDTH // 2 - 30, 10))
            
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    engine = PongEngine()
    player = Players.BotPlayer()
    engine.RunGame(player)
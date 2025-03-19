import pygame
import random
import Players

# Constants
WIDTH, HEIGHT = 900, 600
BALL_SPEED = 5
PADDLE_SPEED = 7
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100

# colors
WHITE       = (255, 255, 255)
BLACK       = (0, 0, 0)
RED         = (255, 0, 0)
GREEN       = (0, 255, 0)
BLUE        = (0, 0, 255)
YELLOW      = (255, 255, 0)
CYAN        = (0, 255, 255)
MAGENTA     = (255, 0, 255)
GRAY        = (128, 128, 128)
DARK_GRAY   = (64, 64, 64)
LIGHT_GRAY  = (192, 192, 192)
ORANGE      = (255, 165, 0)
PURPLE      = (128, 0, 128)
PINK        = (255, 192, 203)
BROWN       = (139, 69, 19)

class PongEngine: 

    def RunGame(self, players):
        pygame.init()
        # Create window
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pong")
        # Ball position & velocity
        ball_x = []
        ball_y = []
        ball_dx = []
        ball_dy = []
        paddle_y = []
        scores = []
        colors = []
        gameFinished = []
        for i in range(len(players)):
            ball_x.append(WIDTH // 2)
            ball_y.append(HEIGHT // 2)
            ball_dx.append(BALL_SPEED)
            #value = random.choice(range(-BALL_SPEED, 0)) if random.random() < 0.5 else random.choice(range(1, BALL_SPEED + 1))
            value = random.choice([-BALL_SPEED, BALL_SPEED])
            ball_dy.append(value)
            paddle_y.append(HEIGHT // 2 - PADDLE_HEIGHT // 2)
            scores.append(0)
            gameFinished.append(False)
            randomColor = random.choice([RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, GRAY, ORANGE, PURPLE, PINK, BROWN])
            colors.append(randomColor)

        print(colors)
        # Game loop
        running = True
        clock = pygame.time.Clock()
        while running:
            screen.fill(BLACK)

            # test if quit pressed
            if pygame.event.peek(pygame.QUIT):
                running = False
                break

            # Update Players
            for i in range(len(players)):
                # skip if player i is finished
                if gameFinished[i] == True:
                    continue
                move = players[i].Update(ball_x[i], ball_y[i], ball_dx[i], ball_dy[i], paddle_y[i] + PADDLE_HEIGHT//2)
                # Update Paddle
                if move == 1:
                    paddle_y[i] += PADDLE_SPEED
                elif move == -1:
                    paddle_y[i] -= PADDLE_SPEED

                # Move ball
                ball_x[i] += ball_dx[i]
                ball_y[i] += ball_dy[i]
                
                # Ball collision with top/bottom
                if ball_y[i] - BALL_RADIUS <= 0:
                    ball_dy[i] *= -1
                    ball_y[i] = BALL_RADIUS + 1
                elif ball_y[i] + BALL_RADIUS >= HEIGHT:
                    ball_dy[i] *= -1
                    ball_y[i] = HEIGHT - BALL_RADIUS - 1
                    
                
                # Ball collision with paddle
                if (ball_x[i] - BALL_RADIUS <= PADDLE_WIDTH and paddle_y[i] < ball_y[i] < paddle_y[i] + PADDLE_HEIGHT and ball_dx[i] < 0):
                    ball_dx[i] *= -1
                    scores[i] += 1
                    ball_dx[i] *= 1.05 # make ball faster
                    ball_dy[i] *= 1.05 # make ball faster
                    # change y speed of ball if not hit in center
                    diffFromCenter = paddle_y[i] + PADDLE_HEIGHT // 2 - ball_y[i]
                    ball_dy[i] += abs(ball_dx[i]) * (diffFromCenter / PADDLE_HEIGHT) * -2
                
                # Ball collision with wall on right side
                if (ball_x[i] + BALL_RADIUS >= WIDTH):
                    ball_dx[i] *= -1
                
                # Paddle out of bounds
                if(paddle_y[i] < 0):
                    paddle_y[i] = 0
                if(paddle_y[i] + PADDLE_HEIGHT > HEIGHT):
                    paddle_y[i] = HEIGHT - PADDLE_HEIGHT

                # Ball out of bounds --> game finished
                if ball_x[i] < 0:
                    gameFinished[i] = True
                    # if all players are finished: return scores
                    if all(gameFinished):
                        return scores
                    continue

                if players[i].visualize == True:
                    pygame.draw.rect(screen, colors[i], (0, paddle_y[i], PADDLE_WIDTH, PADDLE_HEIGHT))
                    pygame.draw.circle(screen, colors[i], (ball_x[i], ball_y[i]), BALL_RADIUS)
            
            # Draw highest score
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {max(scores)}", True, WHITE)
            screen.blit(score_text, (WIDTH // 2 - 30, 10))
            
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    engine = PongEngine()
    player = Players.BotPlayer()
    player2 = Players.BotPlayer()
    humanPlayer = Players.HumanPlayer()
    engine.RunGame([humanPlayer])
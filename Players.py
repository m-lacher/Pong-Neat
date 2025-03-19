import neat
import pygame

class BotPlayer: 
    def __init__(self, visualize = True):
        self.visualize = visualize
    def Update(self, ball_x, ball_y, ball_dx, ball_dy, paddle_y):
        if(ball_y > paddle_y + 10):
            return 1
        if(ball_y < paddle_y - 10):
            return -1
        
class HumanPlayer:
    def __init__(self, visualize = True):
        self.visualize = visualize
    def Update(self, ball_x, ball_y, ball_dx, ball_dy, paddle_y):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            return -1
        if keys[pygame.K_DOWN]:
            return 1
        return 0 

class NeatPlayer:
    def __init__(self, genome, config, visualize=True):
        self.genome = genome
        self.net = neat.nn.FeedForwardNetwork.create(genome, config)
        self.visualize = visualize
    
    def Update(self, ball_x, ball_y, ball_dx, ball_dy, paddle_y):
        # Get response from neural net
        moveUp, moveDown, doNothing = self.net.activate([ball_x, ball_y, ball_dx, ball_dy, paddle_y])
        # Determine the highest output
        max_action = max(moveUp, moveDown, doNothing)
        # Post a fake key event for paddle movement
        if max_action == moveUp:
            return 1
        elif max_action == moveDown:
            return -1
        else:
            return 0

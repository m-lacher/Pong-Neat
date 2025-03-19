import neat
import os
from PongAgainstWall_multiple_players import PongEngine
import Players

def eval_genomes(genomes, config):
    engine = PongEngine()
    players = []
    for id, genome in genomes:
        genome.fitness = 0
        player = Players.NeatPlayer(genome, config)
        players.append(player)

    scores = engine.RunGame(players)
    for i in range(len(scores)):
        players[i].genome.fitness = scores[i]

def run(config_file, checkpoint = None):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    if checkpoint:
        p = neat.Checkpointer.restore_checkpoint(checkpoint)
        #p = restore_checkpoint(checkpoint, config)
        #p.config = config

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 500)
 

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')
    run(config_path)
 
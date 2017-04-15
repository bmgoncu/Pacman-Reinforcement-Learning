from maze_interface import MazeInterface
## My Stuff
from pacman import *
from keyboardAgents import KeyboardAgent
from game import GameStateData
from game import Game
from game import Directions
from game import Actions
from util import nearestPoint
from util import manhattanDistance
import util, layout
## End my stuff

import numpy as np
from numpy.random import random_integers as rand
import matplotlib.pyplot as pyplot
import operator
import cPickle
import os
import logging

WHITE = 255
PLAYER = 170
ENEMY = 127
SUPER_PELLET = 100
PELLET = 85
BLACK = 0
WALL = WHITE
EMPTY_SPACE = BLACK

MAZE_PICKLE_FOLDER = 'maze'

GATE_REWARD = 10

class MazeGenerator(MazeInterface):
    def __init__(self, l="originalClassic", n=60, x=50, timeout=30):
        super(MazeGenerator, self).__init__()
        self.maze_type = l
        self.maze_layout = layout.getLayout(l)
        self.height = self.maze_layout.height
        self.width = self.maze_layout.width

        ## Set Game rule set
        self.rules = ClassicGameRules(timeout)
        ## Set Keyboard Agent
        agentOpts = {}
        agentOpts['numTraining'] = n
        pacmanType = loadAgent("KeyboardAgent", True)
        self.pacmanAgent = pacmanType(**agentOpts)        ## -p parametresi

        ## Aet Ghost Agents
        ghostType = loadAgent("RandomGhost", True)
        self.ghosts = [ghostType(gi + 1) for gi in 4]
        import graphicsDisplay
        self.gameDisplay = graphicsDisplay.PacmanGraphics(1.0, frameTime=0.1)
        self.beQuiet = True
        self.gamesPlayed = []
        self.minimalActionSet = []
        for direction in Actions.getAllPossibleActions():
            self.minimalActionSet.append(Actions.directionToIndex(direction))

    def getScreenDims(self):
        return (self.width + 1) * 3, (self.height + 1) * 3  ## bu pixelmi?

    def getScreenGrayscale(self, screen_data=None):
        ## 84*84 olacak şekilde 27*27 lik bir alanı (28*28)x 3 şeklinde yapıyorum
        H = (self.height + 1)
        W = (self.width + 1)
        if screen_data is None:
            screen_data = np.empty((H * 3, W * 3), dtype=np.uint8)
        for i in range(0, W):
            for j in range(0, H):
                value = BLACK
                if self.maze_layout.isWall(i, j):
                    value = WALL
                else:
                    if self.game.state.hasFood(i,j):
                        value = PELLET
                    else:
                        if self.game.state.hasCapsule(i,j):
                            value = SUPER_PELLET
                        else:
                            value = EMPTY_SPACE
                    for a in range(len(self.game.agents)):
                        agent = self.game.agents[a]
                        if a == 0:
                            value = PLAYER
                        else:
                            value = ENEMY
                X = i * 3
                Y = j * 3
                screen_data[X][Y] = value
                screen_data[X][Y+1] = value
                screen_data[X][Y+2] = value

                screen_data[X+1][Y] = value
                screen_data[X+1][Y+1] = value
                screen_data[X+1][Y+2] = value

                screen_data[X+2][Y] = value
                screen_data[X+2][Y+1] = value
                screen_data[X+2][Y+2] = value

        return screen_data

    def act(self, action_index):
        return self.game.runOneStep(action_index)

        ## game.run fonksionunu içinde bir step olacak şekilde
        ##action = maze_actions.get_action(action_index).value
        ##next_pos = tuple(map(operator.add, self.agent_pos, action))
        ##if self.maze[next_pos[1]][next_pos[0]] != WALL:
        ##    self.agent_pos = next_pos

        ##self.action_count += 1
        ##if self.agent_pos == self.target_pos:  # end episode
        ##    rwrd = 100 - self.reward_given
        ##    self.reward_given = 100
        ##    return rwrd
        ##elif self.check_gate_reward():
        ##    self.reward_given += GATE_REWARD
        ##    return GATE_REWARD
        ##else:
        ##    return 0

    def reset_game(self):
        self.game = self.rules.newGame(layout, self.pacmanAgent, self.ghosts, self.gameDisplay, self.beQuiet, False)
        if not self.beQuiet:
            self.gamesPlayed.append(self.game)

        self.action_count = 0
        self.reward_given = 0

    def game_over(self):
        return self.game.gameOver

    def lives(self):
        return 1

    def getMinimalActionSet(self):
        return self.minimalActionSet

    def getLegalActionSet(self):
        #self.PacmanRules.getLegalActions() var amaaaaa
        ##return self.game.state.getLegalActions(0)
        return self.minimalActionSet

    def getScreenRGB(self):
        gray = self.getScreenGrayscale()
        vis = np.empty((gray.shape[0], gray.shape[1], 3), np.uint8)
        vis[:, :, 0] = gray
        vis[:, :, 1] = gray
        vis[:, :, 2] = gray
        return vis

if __name__ == "__main__":
    m = MazeGenerator("originalClassic", 60, 50)
    m.reset_game()
    i = 0
    while (not m.game_over() and i < 0):
        action = rand(0, 3)
        prev = m.agent_pos
        r = m.act(action)
        next_state = m.agent_pos
        #print("{} -- {} --> {} {}".format(prev, maze_actions.get_action(action).name, next_state, r))
        i += 1
    m.reset_game()
    print m.agent_pos
    print m.target_pos
    print m.check_opposite_sides()
    print m.areas
    pyplot.figure(figsize=(10, 5))
    pyplot.imshow(m.getScreenRGB(), cmap='Greys_r', interpolation='nearest')
    pyplot.imshow(m.getScreenRGB(), cmap='Greys_r', interpolation='nearest')
    pyplot.xticks([]), pyplot.yticks([])
    pyplot.show()

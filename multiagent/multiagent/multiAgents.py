# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util
import numpy as np

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        ghostDist = sum([manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates])
        try: foodDist = min([manhattanDistance(newPos, foodPos) for foodPos in newFood.asList()])
        except: foodDist = 0

        return successorGameState.getScore() + 2 * min(8, ghostDist) + 10/(1+foodDist)

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    def minimax_value(self, gameState, depth, agent):
        if depth == 0 or not bool(gameState.getLegalActions(agent)): return self.evaluationFunction(gameState)

        if agent == 0: # Pacman is playing - aiming to maximise its own payoffs
            maxV = float('-inf')
            next_agent = agent + 1;

            for action in gameState.getLegalActions(agent):
                value = self.minimax_value(gameState.generateSuccessor(agent, action), depth, next_agent)
                maxV = max(value, maxV)
            return maxV

        else: # Ghosts are playing - aiming to minimise the payoff to PacMan
            minV = float('inf')
            if (int(agent) + 1) == int(gameState.getNumAgents()): depth -= 1; next_agent = 0
            else: next_agent = agent + 1

            for action in gameState.getLegalActions(agent):
                value = self.minimax_value(gameState.generateSuccessor(agent, action), depth, next_agent)
                minV = min(value, minV)
            return minV

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        agent = self.index; depth = self.depth

        if (int(agent) + 1) == int(gameState.getNumAgents()): next_agent = 0
        else: next_agent = agent + 1

        return max(gameState.getLegalActions(agent),
                   key=lambda action: self.minimax_value(gameState.generateSuccessor(agent, action), depth, next_agent))

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def max_value(self, gameState, alpha, beta, depth, agent):
        if depth == 0 or not bool(gameState.getLegalActions(agent)): return self.evaluationFunction(gameState)

        next_agent = agent + 1

        v = float('-inf')
        for action in gameState.getLegalActions(agent):
            v = max(v, self.min_value(gameState.generateSuccessor(agent, action), alpha, beta, depth, next_agent))
            alpha = max(v, alpha)
            '''
            If it turns out that the minimum score that the maximising player can get (beta) is higher than the highest possible
            score that he can obtain from another subtree (alpha) - subject to his opponent's play, and it is currently his turn,
            there's no need to evaluate the subtree, as his opponent will force him to get the lowest possible score.
            '''
            if beta < alpha: break
        return v

    def min_value(self, gameState, alpha, beta, depth, agent):
        if depth == 0 or not bool(gameState.getLegalActions(agent)): return self.evaluationFunction(gameState)

        v = float('inf')
        if (int(agent) + 1) == int(gameState.getNumAgents()): depth -= 1; next_agent = 0
        else: next_agent = agent + 1

        for action in gameState.getLegalActions(agent):
            if next_agent > 0: # Ghost's turn to move **again**...
                v = min(v, self.min_value(gameState.generateSuccessor(agent, action), alpha, beta, depth, next_agent))
            else: # Pacman's turn to move!
                v = min(v, self.max_value(gameState.generateSuccessor(agent, action), alpha, beta, depth, next_agent))
            beta = min(v, beta)
            '''
            If it turns out that the highest possible score that our player can obtain by playing in another subtree (alpha) is
            higher than that of the minimum score that the maximising player is guaranteed of (beta), and it is the opponent's turn,
            we do not have to evaluate the subtree as the opponent will ensure that we will never get to the subtree.
            '''
            if beta < alpha: break
        return v

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # Initializing alpha and beta values
        alpha = float('-inf') # Minimum value that PacMan can get
        beta = float('inf') # Maximum value that PacMan can get
        agent = self.index; depth = self.depth

        best_score, best_action = float('-inf'), None
        v = float('-inf')

        for action in gameState.getLegalActions(agent):
            v = max(v, self.min_value(gameState.generateSuccessor(agent, action), alpha, beta, depth, agent+1))
            if best_score < v:
                best_score = v
                best_action = action

            alpha = max(v, alpha)
            if beta < alpha: break

        return best_action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def max_value(self, gameState, depth, agent): # Pacman's turn to move!
        v = float('-inf')
        for action in gameState.getLegalActions(agent):
            v = max(v, self.value(gameState.generateSuccessor(agent, action), depth, 1))
        return v

    def exp_value(self, gameState, depth, agent):
        if (int(agent) + 1) == int(gameState.getNumAgents()): next_agent = 0; depth -= 1
        else: next_agent = agent + 1

        v = 0
        p = 1/float(len(gameState.getLegalActions(agent)))
        for action in gameState.getLegalActions(agent):
            v += p * self.value(gameState.generateSuccessor(agent, action), depth, next_agent)
        return v

    def value(self, gameState, depth, agent):
        if depth == 0 or not bool(gameState.getLegalActions(agent)): return self.evaluationFunction(gameState)

        # Does pacman or a ghost move next?
        if agent > 0: return self.exp_value(gameState, depth, agent)
        else: return self.max_value(gameState, depth, agent)

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        agent = self.index; depth = self.depth
        next_agent = agent + 1

        return max(gameState.getLegalActions(agent),
                   key=lambda action: self.value(gameState.generateSuccessor(agent, action), depth, next_agent))

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    '''
    First, we conduct K-means clustering of our food coordinates to get 2 different clusters of food locations.
    Depending on which food cluster is closer to PacMan, conditional on how close each food cluster is to the ghosts,
    we will make a decision to decide which food to consume.
    '''
    pacmanPos = currentGameState.getPacmanPosition()

    try: min_dist_from_food = min([manhattanDistance(pacmanPos, foodPos) for foodPos in currentGameState.getFood().asList()])
    except: min_dist_from_food = 0

    mean_dist_from_ghosts = np.mean([manhattanDistance(pacmanPos, foodPos) for foodPos in currentGameState.getFood().asList()])
    return currentGameState.getScore() + 10/(0.01+min_dist_from_food) + 20/(0.01+currentGameState.getFood().count()) - 5/min(5, mean_dist_from_ghosts)

# Abbreviation
better = betterEvaluationFunction

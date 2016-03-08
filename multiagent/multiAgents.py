# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

# This file has been modified by Arjun Devarajan

from util import manhattanDistance
from game import Directions
import random, util

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
    # successorGameState returns a printed map of where all the objects in the
    # game board are: .'s are pieces of food, G is the ghost, % is the walls, 
    # and ^/v/</> is the Pacman
    newPos = successorGameState.getPacmanPosition()
    # newPos returns a (x,y) coordinate of where Pacman is currently
    newFood = successorGameState.getFood()
    # returns a printed map of where all the food is located as "T" and where
    # it's not as "F"
    newGhostStates = successorGameState.getGhostStates()
    # newGhostStates just returns an instance of the agentState
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    # newScaredTimes returns a 0 when the ghost is not scared (when Pacman has
    # not eaten a power pellet) and 40(?) when the ghost is first scared. After
    # Pacman eats the power pellet the ghost gets steadily less scared (--1 every
    # move until it is no longer scared and the power pellet's power has run out

    "*** YOUR CODE HERE ***"
    distances = []
    foodList = newFood.asList()
    for food in foodList:
      distances.append(manhattanDistance(newPos,food))
    ghostDistance = newFood.height + newFood.width
    for ghost in newGhostStates:
        ghostDistance = min(ghostDistance, manhattanDistance(newPos, ghost.getPosition()))
    closestFood = 0
    if foodList:
        closestFood = min(distances)
    if ghostDistance>1:
        return 100*(newFood.width*newFood.height - len(foodList)) + newFood.height + newFood.width - closestFood
    return ghostDistance

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
  def getAction(self, gameState):
    
    # The worst possible minimax score
    bestScore = float("-inf")
    # The worst possible action
    bestAction = "Stop"
    # The total number of ghosts in the game, to be indexed through later
    ghosts = gameState.getNumAgents() - 1

    # Find the minimum value on a level
    def minimum(currentGameState, ghostNum, currentDepth):
      # Set the best possible value to be the highest possible one, infinity
      bestValue = float("inf")
      # Check if the we're at 1) a leaf node, 2) a win, or 3) a loss
      if (currentDepth == 0 or currentGameState.isWin() or currentGameState.isLose()):
          # If so, return the heuristic of that node
          return self.evaluationFunction(currentGameState)
      # If you've cycled through every level of ghosts
      if (ghosts==ghostNum):
          # Then cycle through all the possible actions of the ghost
          for currentAction in currentGameState.getLegalActions(ghostNum):
              # Check what the most recent max is
              currentValue = maximum(currentGameState.generateSuccessor(ghostNum, currentAction), currentDepth - 1)
              # And find the minimum of that
              bestValue = min(bestValue, currentValue)
      else:
          # If you're still looking through the ghosts, chycle through the rest of them
          for currentAction in currentGameState.getLegalActions(ghostNum):
              # Recursively call the minimum function with the ghost index incremented by 1
              currentValue = minimum(currentGameState.generateSuccessor(ghostNum, currentAction), ghostNum + 1, currentDepth)
              # Still, find the minimum at that point
              bestValue = min(bestValue, currentValue)
      return bestValue

    # Find the maximum values on a level
    def maximum(currentGameState, currentDepth):
      # Set the best possible value to be the lowest possible one, negative infinity
      bestValue = float("-inf")
      # Check if we're at a leaf node (can't be a win/loss on Pacman's turn)
      if (currentDepth == 0):
          return self.evaluationFunction(currentGameState)
      # The rest of this method follows structurally similarly to the last one
      for currentAction in currentGameState.getLegalActions(0):
          # One difference: always call the minimum (ghosts) instead of sometimes calling itself
          currentValue = minimum(currentGameState.generateSuccessor(0, currentAction), 1, currentDepth)
          # Always find the max value because we're at a single max level
          bestValue = max(bestValue, currentValue)
      return bestValue

    # To begin searching, look through all the possible actions and 
    for currentAction in gameState.getLegalActions():
        # Check the scores of them
        oldScore = bestScore
        bestScore = max(bestScore, minimum(gameState.generateSuccessor(0, currentAction), 1, self.depth))
        # If an old score is worse than the newest one, then replace that one
        if (oldScore<bestScore):
            bestAction = currentAction
    return bestAction


class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    # Very similar structurally to the previous class, except for the addition of alpha and beta testers
    bestScore = float("-inf")
    bestAction = "Stop"
    ghosts = gameState.getNumAgents() - 1
    def minimum(currentGameState, ghostNum, currentDepth, alpha, beta):
      bestValue = float("inf")
      if (currentDepth == 0 or currentGameState.isWin() or currentGameState.isLose()):
          return self.evaluationFunction(currentGameState)
      if (ghosts==ghostNum):
          for currentAction in currentGameState.getLegalActions(ghostNum):
              currentValue = maximum(currentGameState.generateSuccessor(ghostNum, currentAction), currentDepth - 1, alpha, beta)
              # Test to see if the minimum is less than the alpha pruner
              if (min(bestValue,currentValue)<=alpha):
                # If it is, then take the minimum to be beta, and if not, skip it entirely
                bestValue = min(bestValue, currentValue)
                beta = min(beta, bestValue)
      else:
          for currentAction in currentGameState.getLegalActions(ghostNum):
              currentValue = minimum(currentGameState.generateSuccessor(ghostNum, currentAction), ghostNum + 1, currentDepth, alpha, beta)
              if (min(bestValue,currentValue)<=alpha):
                bestValue = min(bestValue, currentValue)
                beta = min(beta, bestValue)
      return bestValue

    def maximum(currentGameState, currentDepth, alpha, beta):
      bestValue = float("-inf")
      if (currentDepth == 0):
          return self.evaluationFunction(currentGameState)
      for currentAction in currentGameState.getLegalActions(0):
          currentValue = minimum(currentGameState.generateSuccessor(0, currentAction), 1, currentDepth, alpha, beta)
          # Alternately, test to see if the maximum is greater than the beta pruner
          if (max(bestValue,currentValue)>=beta):
                # If it is, then take the minimum here to be alpha, and if not, skip it entirely
                bestValue = max(bestValue, currentValue)
                alpha = min(alpha, bestValue)
      return bestValue
    # Initially set alpha and beta pruners to be the lowest/highest possible numbers
    alpha = float("-inf")
    beta = float("inf")
    for currentAction in gameState.getLegalActions():
        oldScore = bestScore
        bestScore = max(bestScore, minimum(gameState.generateSuccessor(0, currentAction), 1, self.depth, alpha, beta))
        if (oldScore<bestScore):
            bestAction = currentAction
    return bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"  
    # Once again, very structurally similar to the previous 2 classes, with the notable
    # removal of the minimum method and the addition of the expected method to calculate
    # an "expected value" for the ghosts to more accurately represent their trajectories
    bestScore = float("-inf")
    bestAction = "Stop"
    ghosts = gameState.getNumAgents() - 1
    # Find the exapected values
    def expected(currentGameState, ghostNum, currentDepth):
      # Set what the total value will be
      bestValue = 0
      if (currentDepth == 0 or currentGameState.isWin() or currentGameState.isLose()):
          return self.evaluationFunction(currentGameState)
      if (ghosts==ghostNum):
          for currentAction in currentGameState.getLegalActions(ghostNum):
              # Add up the maximum of each possible Pacman action
              bestValue += maximum(currentGameState.generateSuccessor(ghostNum, currentAction), currentDepth - 1)
      else:
          for currentAction in currentGameState.getLegalActions(ghostNum):
              # Otherwise, add up the expected value of each other additional ghost action
              bestValue += expected(currentGameState.generateSuccessor(ghostNum, currentAction), ghostNum + 1, currentDepth)
      # In the end, find the expected value by taking the total/the length
      return bestValue/len(currentGameState.getLegalActions(ghostNum))

    def maximum(currentGameState, currentDepth):
      bestValue = float("-inf")
      if (currentDepth == 0):
          return self.evaluationFunction(currentGameState)
      for currentAction in currentGameState.getLegalActions(0):
          # Find the expected value when switching back and forth between Pacman/ghosts
          currentValue = expected(currentGameState.generateSuccessor(0, currentAction), 1, currentDepth)
          bestValue = max(bestValue, currentValue)
      return bestValue

    for currentAction in gameState.getLegalActions(0):
        oldScore = bestScore
        # This time, begin by taking the expected value and starting the chain off like that
        bestScore = max(bestScore, expected(gameState.generateSuccessor(0, currentAction), 1, self.depth))
        if (oldScore<bestScore):
            bestAction = currentAction
    return bestAction

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


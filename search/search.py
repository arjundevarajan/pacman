# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

# This file has been modified by Arjun Devarajan

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first
  [2nd Edition: p 75, 3rd Edition: p 87]
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm 
  [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  "*** YOUR CODE HERE ***"

  # First import the Stack class from util and import the directions from game
  from util import Stack
  import copy

  # Set the current state and its actions to variables
  currentState = problem.getStartState()
  currentStateActions = []

  # Store those variables in an immutable node tuple
  currentNode = (currentState,currentStateActions)

  # Create a stack of all the possible states and push the first node into it
  stackOfStates = Stack()
  stackOfStates.push(currentNode)

  # Create a list of all the states that have been visited already
  finishedStates = [currentState]

  # Set a Boolean value for the final goal to have been reached
  finalGoal = False

  # While we haven't reached the goal state yet
  while(not finalGoal):
    
    # Pop the first node off of the stack and assign its values to variables
    currentNode = stackOfStates.pop()
    currentState = currentNode[0]
    currentStateActions = copy.copy(currentNode[1])

    # If the current state is the goal state, set final goal = true
    if (problem.isGoalState(currentState)):
      finalGoal = True

    else:
      # Address all the successors of the current node
      currentSuccessors = problem.getSuccessors(currentState)

      # For each of the successors of the current node
      for nextSuccessor in currentSuccessors:
        
        # Separate out the state and the actions of this successor
        nextState = nextSuccessor[0]
        nextStateAction = copy.copy(nextSuccessor[1])

        # Make a temporary copy of the set of actions so that it can be added to later with the action of the successor
        tempCSA = copy.copy(currentStateActions)

        # If this state has not been searched yet
        if (nextState not in finishedStates):
          # Add the next state's action to the list of actions
          finishedStates.append(nextState)
          tempCSA.append(nextStateAction)

          # Create a node for the state and push it to the stack
          newNode = (nextState,tempCSA)
          stackOfStates.push(newNode)

  # Once we've reached the goal state, return the list of actions
  return currentStateActions

  util.raiseNotDefined()

def breadthFirstSearch(problem):
  """
  Search the shallowest nodes in the search tree first.
  [2nd Edition: p 73, 3rd Edition: p 82]
  """
  "*** YOUR CODE HERE ***"
  ## The only difference between this problem and the previous DFS method is the use of a Queue rather than a Stack

  # First import the Queue class from util and import the directions from game
  from util import Queue
  import copy

  # Set the current state and its actions to variables
  currentState = problem.getStartState()
  currentStateActions = []

  # Store those variables in an immutable node tuple
  currentNode = (currentState,currentStateActions)

  # Create a queue of all the possible states and push the first node into it
  queueOfStates = Queue()
  queueOfStates.push(currentNode)

  # Create a list of all the states that have been visited already
  finishedStates = [currentState]

  # Set a Boolean value for the final goal to have been reached
  finalGoal = False

  # While we haven't reached the goal state yet
  while(not finalGoal):
    
    # Pop the first node off of the queue and assign its values to variables
    currentNode = queueOfStates.pop()
    currentState = currentNode[0]
    currentStateActions = copy.copy(currentNode[1])

    # If the current state is the goal state, set final goal = true
    if (problem.isGoalState(currentState)):
      finalGoal = True

    else:
      # Address all the successors of the current node
      currentSuccessors = problem.getSuccessors(currentState)

      # For each of the successors of the current node
      for nextSuccessor in currentSuccessors:
        
        # Separate out the state and the actions of this successor
        nextState = nextSuccessor[0]
        nextStateAction = copy.copy(nextSuccessor[1])

        # Make a temporary copy of the set of actions so that it can be added to later with the action of the successor
        tempCSA = copy.copy(currentStateActions)

        # If this state has not been searched yet
        if (nextState not in finishedStates):
          # Add the next state's action to the list of actions
          finishedStates.append(nextState)
          tempCSA.append(nextStateAction)

          # Create a node for the state and push it to the queue
          newNode = (nextState,tempCSA)
          queueOfStates.push(newNode)

  # Once we've reached the goal state, return the list of actions
  return currentStateActions
  util.raiseNotDefined()
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  # The main difference between this problem and the ones previously is the use of a Priority Queue in conjunction with a total cost value being calculated at all times

  # First import the PriorityQueue class from util and import the directions from game
  from util import PriorityQueue
  import copy

  # Set the current state and its actions and cost to variables
  currentState = problem.getStartState()
  currentStateActions = []
  currentCost = 0

  # Store those variables in an immutable node tuple
  currentNode = (currentState,currentStateActions, currentCost)

  # Create a priority queue of all the possible states and push the first node into it
  priorityQueueOfStates = PriorityQueue()
  priorityQueueOfStates.push(currentNode, currentCost)

  # Create a list of all the states that have been visited already
  finishedStates = [currentState]

  # Set a Boolean value for the final goal to have been reached
  finalGoal = False

  # While we haven't reached the goal state yet
  while(not finalGoal):
    
    # Pop the first node off of the priority queue and assign its values to variables
    currentNode = priorityQueueOfStates.pop()
    currentState = currentNode[0]
    currentStateActions = copy.copy(currentNode[1])
    currentCost = currentNode[2]

    # If the current state is the goal state, set final goal = true
    if (problem.isGoalState(currentState)):
      finalGoal = True

    else:
      # Address all the successors of the current node
      currentSuccessors = problem.getSuccessors(currentState)

      # For each of the successors of the current node
      for nextSuccessor in currentSuccessors:
        
        # Separate out the state and the actions of this successor
        nextState = nextSuccessor[0]
        nextStateAction = copy.copy(nextSuccessor[1])
        nextCost = nextSuccessor[2]

        # Add the successor's cost to the cost so far
        newCost = nextCost + currentCost

        # Make a temporary copy of the set of actions so that it can be added to later with the action of the successor
        tempCSA = copy.copy(currentStateActions)

        # If this state has not been searched yet
        if (nextState not in finishedStates):
          # Add the next state's action to the list of actions
          finishedStates.append(nextState)
          tempCSA.append(nextStateAction)

          # Create a node for the state and push it to the priority queue
          newNode = (nextState,tempCSA,newCost)
          priorityQueueOfStates.push(newNode,newCost)

  # Once we've reached the goal state, return the list of actions
  return currentStateActions
  util.raiseNotDefined()

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  # The main difference between this problem and the ones previously is the use of a Priority Queue
  # in conjunction with a total cost value and a heuristic function being calculated at all times

  # First import the PriorityQueue class from util and import the directions from game
  from util import PriorityQueue
  import copy

  # Set the current state and its actions and cost to variables
  currentState = problem.getStartState()
  currentStateActions = []
  # currentCost = 0
  currentCost = problem.getCostOfActions(currentStateActions)

  # Store those variables in an immutable node tuple
  currentNode = (currentState,currentStateActions, currentCost)

  # Create a priority queue of all the possible states and push the first node into it
  priorityQueueOfStates = PriorityQueue()
  priorityQueueOfStates.push(currentNode, currentCost)

  # Create a list of all the states that have been visited already
  finishedStates = [currentState]

  # Set a Boolean value for the final goal to have been reached
  finalGoal = False

  # While we haven't reached the goal state yet
  while(not finalGoal):
    
    # Pop the first node off of the priority queue and assign its values to variables
    currentNode = priorityQueueOfStates.pop()
    currentState = currentNode[0]
    currentStateActions = copy.copy(currentNode[1])
    currentCost = currentNode[2]

    # If the current state is the goal state, set final goal = true
    if (problem.isGoalState(currentState)):
      finalGoal = True

    else:
      # Address all the successors of the current node
      currentSuccessors = problem.getSuccessors(currentState)

      # For each of the successors of the current node
      for nextSuccessor in currentSuccessors:
        
        # Separate out the state and the actions of this successor
        nextState = nextSuccessor[0]
        nextStateAction = copy.copy(nextSuccessor[1])
        nextCost = nextSuccessor[2]

        # Find out how much the heuristic function cost is
        hCost = heuristic(nextState,problem)

        # Add the successor's cost to the cost so far
        newCost = currentCost + nextCost + hCost

        # Make a temporary copy of the set of actions so that it can be added to later with the action of the successor
        tempCSA = copy.copy(currentStateActions)

        # If this state has not been searched yet
        if (nextState not in finishedStates):
          # Add the next state's action to the list of actions
          finishedStates.append(nextState)
          tempCSA.append(nextStateAction)

          # Create a node for the state and push it to the priority queue
          newNode = (nextState,tempCSA,newCost)
          priorityQueueOfStates.push(newNode,newCost)

  # Once we've reached the goal state, return the list of actions
  return currentStateActions
  util.raiseNotDefined()
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

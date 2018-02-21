# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import copy

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    # Create data structures to store information on the explored nodes, actions taken and successor states
    frontier = util.Stack()
    explored_set = set(); action_dict = {}

    startState = problem.getStartState()
    frontier.push([startState])

    while True:
        if frontier.isEmpty(): return False
        path = frontier.pop(); s = path[-1]
        explored_set.add(s)

        try: current_action_list = action_dict[s]
        except: current_action_list = []

        if problem.isGoalState(s): return current_action_list

        for successor, action, cost in problem.getSuccessors(s):
            if (successor in explored_set): continue

            frontier.push(path + [successor])
            action_dict[successor] = current_action_list + [action]

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # Create data structures to store information on the explored nodes, actions taken and successor states
    frontier = util.Queue(); frontier_path = set()
    explored_set = set(); frontier_set = set()

    startState = problem.getStartState()
    # Let's set the frontier as a tuple consisting of the current state, existing path and path cost
    frontier.push((startState, [], 0))

    while True:
        if frontier.isEmpty(): return False
        (_state, _path, _cost) = frontier.pop();
        explored_set.add(_state)

        if problem.isGoalState(_state): return _path

        for successor, action, cost in problem.getSuccessors(_state):
            if (successor in explored_set) or (successor in frontier_set): continue

            frontier.push((successor, _path + [action], _cost + cost)); frontier_set.add(successor)

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # Create data structures to store information on the explored nodes, actions taken and successor states
    frontier = util.PriorityQueue()
    explored_set = set(); frontier_set = set()
    cost_dict = util.Counter(); action_dict = {}

    current_cost = float('inf'); current_solution = []

    startState = problem.getStartState()
    # The cost at the initial state is 0
    frontier.push([startState], 0)

    while True:
        if frontier.isEmpty(): return current_solution
        path = frontier.pop(); s = path[-1]
        explored_set.add(s)

        if cost_dict[s] > current_cost: return current_solution
        try: current_action_list = action_dict[s]
        except: current_action_list = []

        if problem.isGoalState(s):
            if cost_dict[s] < current_cost:
                current_cost, current_solution = cost_dict[s],  action_dict[s]

                if frontier.isEmpty(): return current_solution
                path = frontier.pop(); s = path[-1]
                explored_set.add(s)

                if cost_dict[s] >= current_cost: return current_solution
                current_action_list = action_dict[s]

        for successor, action, cost in problem.getSuccessors(s):
            total_cost = cost_dict[s] + cost

            if (successor not in explored_set) and (successor not in frontier_set):
                cost_dict[successor] = total_cost
                frontier.push(path + [successor], total_cost); frontier_set.add(successor)
                action_dict[successor] = current_action_list + [action]
            else:
                if cost_dict[successor] > total_cost:
                    cost_dict[successor] = total_cost
                    frontier.push(path + [successor], total_cost)
                    action_dict[successor] = current_action_list + [action]


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # Create data structures to store information on the explored nodes, actions taken and successor states
    frontier = util.PriorityQueue()
    explored_set = set(); frontier_set = set()
    cost_dict = util.Counter(); heuristic_cost_dict = util.Counter()
    action_dict = {}

    current_cost = float('inf'); current_solution = []

    startState = problem.getStartState()
    # The cost at the initial state is 0
    frontier.push([startState], 0)

    while True:
        if frontier.isEmpty(): return current_solution
        path = frontier.pop(); s = path[-1]
        explored_set.add(s)

        if cost_dict[s] > current_cost: return current_solution
        try: current_action_list = action_dict[s]
        except: current_action_list = []

        if problem.isGoalState(s):
            if cost_dict[s] < current_cost:
                current_cost, current_solution = cost_dict[s],  action_dict[s]

                if frontier.isEmpty(): return current_solution
                path = frontier.pop(); s = path[-1]
                explored_set.add(s)

                if cost_dict[s] + heuristic(s, problem) >= current_cost: return current_solution
                current_action_list = action_dict[s]

        for successor, action, cost in problem.getSuccessors(s):
            path_cost = cost_dict[s] + cost
            heuristic_cost = heuristic(successor, problem)

            if (successor not in explored_set) and (successor not in frontier_set):
                cost_dict[successor] = path_cost
                frontier.push(path + [successor], path_cost + heuristic_cost); frontier_set.add(successor)
                action_dict[successor] = current_action_list + [action]

            else:
                if cost_dict[successor] > path_cost:
                    cost_dict[successor] = path_cost
                    frontier.push(path + [successor], path_cost + heuristic_cost)
                    action_dict[successor] = current_action_list + [action]

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

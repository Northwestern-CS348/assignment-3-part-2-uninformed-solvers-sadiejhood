
from solver import *
from logical_classes import *
import queue


class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.visited_states = {
            ((1, 2, 3), (), ()): False,
            ((2, 3), (1,), ()): False,
            ((2, 3), (), (1,)): False,
            ((3,), (1,), (2,)): False,
            ((3,), (2,), (1,)): False,
            ((3,), (1, 2), ()): False,
            ((3,), (), (1,2)): False,
            ((), (1, 2), (3)): False,
            ((3,), (1, 2), ()): False,
            ((), (3,), (1,2)): False,
            ((3,), (), (1,2)): False,
            ((1, 2), (), (3,)): False,
            ((1, 2), (3,), ()): False,
            ((), (1, 2, 3), ()): False,
            ((), (), (1, 2, 3)): False
        }

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here

        if (self.currentState.state == self.victoryCondition):
            return True

        if (self.currentState.children == []):
            moveFromHere = self.gm.getMovables()
            for m in moveFromHere:
                self.gm.makeMove(m)
                new_state = GameState(self.gm.getGameState(), self.currentState.depth+1, m)
                new_state.requiredMovable = m
                self.gm.reverseMove(m)
                new_state.parent = self.currentState
                self.visited[new_state] = False

                # print(new_state.state)
                if ( (new_state.state in self.visited_states) and self.visited_states[new_state.state] == False):
                    self.currentState.children.append(new_state)
                    # print("New State " + str(new_state.state))
                    # print("Depth " + str(self.currentState.depth + 1))
                    # print("Parent " + str(new_state.parent.requiredMovable))
                    # print('\n')
                elif (not self.currentState.parent):
                    self.currentState.children.append(new_state)
                    # print("New State " + str(new_state.state))
                    # print("Depth " + str(self.currentState.depth + 1))
                    # print("Parent " + str(new_state.parent.requiredMovable))
                    # print('\n')

        if (self.currentState.nextChildToVisit + 1 > len(self.currentState.children)):
            # print(self.currentState.state)
            # print(self.currentState.requiredMovable)
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            return False

        if ((len(self.currentState.children) > 0) and not self.visited[self.currentState.children[self.currentState.nextChildToVisit]] == True):
            # print("Wow")
            self.gm.makeMove(self.currentState.children[self.currentState.nextChildToVisit].requiredMovable)
            self.visited[self.currentState.children[self.currentState.nextChildToVisit - 1]] = True
            self.visited_states[self.currentState.state] = True
            self.currentState.nextChildToVisit += 1
            self.currentState = self.currentState.children[self.currentState.nextChildToVisit - 1]
            # print(self.currentState.requiredMovable)
            return False
        else:
            # print("wow2")
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            return False


        # print(self.currentState.requiredMovable)
        # self.gm.reverseMove(self.currentState.requiredMovable)
        # self.currentState = self.currentState.parent
        # return False



        # self.gm.kb_reverseMove(self.currentState.requiredMovable)
        # return

        # # stack - can just use a list
        # self.currentState.children = []
        # # print(self.gm.getMovables())
        # if (self.gm.getMovables()):
        #     for el in self.gm.getMovables():
        #         self.currentState.children.append(el)
        #
        # for el in self.currentState.children:
        #     if (not el in self.gm.getMovables()):
        #         del el


        # print(self.currentState.children[1])

        # if( len(self.currentState.children) == 0 ):
        #     return False
        #
        # while (len(self.currentState.children) != 0):
        #     new_state = GameState(self.gm.getGameState(), self.currentState.depth+1, self.currentState.children[0])
        #     new_state.parent = self.currentState
        #     new_state.children = self.currentState.children
        #
        #     if (type(self.currentState.children) is list):
        #         new_move = self.currentState.children[0]
        #     else:
        #         new_move = self.currentState.children
        #
        #     self.currentState.children.pop(0)
        #     new_state.children = self.currentState.children
        #     # print(new_move)
        #
        #     self.gm.makeMove(new_move)
        #     new_state.state = self.gm.getGameState()
        #
        #     if (self.gm.isWon()):
        #         return True
        #     else:
        #         return




class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        # stack - can just use a list
        self.currentState.children = []
        # print(self.gm.getMovables())
        if (self.gm.getMovables()):
            for el in self.gm.getMovables():
                self.currentState.children.append(el)

        for el in self.currentState.children:
            if (not el in self.gm.getMovables()):
                del el


        # print(self.currentState.children[1])

        if( len(self.currentState.children) == 0 ):
            return False

        while (len(self.currentState.children) != 0):
            new_state = GameState(self.gm.getGameState(), self.currentState.depth+1, self.currentState.children[0])
            new_state.parent = self.currentState
            new_state.children = self.currentState.children

            # print(self.visited[new_state])

            if (not self.visited[new_state]):
                self.currentState.children.pop(0)
            else:
                if (type(self.currentState.children) is list):
                    new_move = self.currentState.children[0]
                else:
                    new_move = self.currentState.children

                self.currentState.children.pop(0)
                new_state.children = self.currentState.children
                # print(new_move)

                self.gm.makeMove(new_move)
                new_state.state = self.gm.getGameState()

                if (self.gm.isWon()):
                    return True
                else:
                    return

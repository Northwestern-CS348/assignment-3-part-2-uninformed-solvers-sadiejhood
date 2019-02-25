from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        facts = self.kb.facts
        # for f in facts:
        #     print(f)
        #
        # print('\n\n\n')

        elements_on = []
        state = Statement(["on", "?x", "?y"])

        for f in facts:
            if (match(state, f.statement) ):
                elements_on.append(f)

        gameState = [[], [], []]

        for el in elements_on:
            bindings = match(state, el.statement)
            # print(str(bindings) + " =?= ?X : disk1, ?Y : peg1")
            # print(str(bindings) == "?X : disk1, ?Y : peg1")

            if (str(bindings) == "?X : disk1, ?Y : peg1"):
                gameState[0].append(1)
            elif (str(bindings) == "?X : disk2, ?Y : peg1"):
                gameState[0].append(2)
            elif (str(bindings) == "?X : disk3, ?Y : peg1"):
                gameState[0].append(3)
            elif (str(bindings) == "?X : disk4, ?Y : peg1"):
                gameState[0].append(4)
            elif (str(bindings) == "?X : disk5, ?Y : peg1"):
                gameState[0].append(5)
            elif (str(bindings) == "?X : disk1, ?Y : peg2"):
                gameState[1].append(1)
            elif (str(bindings) == "?X : disk2, ?Y : peg2"):
                gameState[1].append(2)
            elif (str(bindings) == "?X : disk3, ?Y : peg2"):
                gameState[1].append(3)
            elif (str(bindings) == "?X : disk4, ?Y : peg2"):
                gameState[1].append(4)
            elif (str(bindings) == "?X : disk5, ?Y : peg2"):
                gameState[1].append(5)
            elif (str(bindings) == "?X : disk1, ?Y : peg3"):
                gameState[2].append(1)
            elif (str(bindings) == "?X : disk2, ?Y : peg3"):
                gameState[2].append(2)
            elif (str(bindings) == "?X : disk3, ?Y : peg3"):
                gameState[2].append(3)
            elif (str(bindings) == "?X : disk4, ?Y : peg3"):
                gameState[2].append(4)
            elif (str(bindings) == "?X : disk5, ?Y : peg3"):
                gameState[2].append(5)

        gameState[0].sort()
        gameState[1].sort()
        gameState[2].sort()

        ## Create the string rep for the gameState
        gameState[0] = tuple(gameState[0])
        gameState[1] = tuple(gameState[1])
        gameState[2] = tuple(gameState[2])
        return_string = tuple(gameState)

        return return_string

        pass

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """

        retracted = []
        added = []
        facts = self.kb.facts
        print(self.getGameState())
        for f in facts:
            if(f.statement.predicate == "movable"):
                print(f)
        print("\n")

        # fs = self.getMovables()
        #
        # self.getGameState()
        # for f in fs:
        #     print(f)

        new_location = movable_statement.terms[2]
        object = movable_statement.terms[0]
        old_location = movable_statement.terms[1]

        old_stack = self.kb.kb_ask(Fact(Statement(["onTopOf", object, "?X"])))
        new_is_empty = self.kb.kb_ask(Fact(Statement(["empty", new_location])))
        new_stack = self.kb.kb_ask(Fact(Statement(["on", "?x", new_location])))

        # print(old_stack.list_of_bindings[0][0].bindings_dict["?X"])
        # print("OLD")
        # print(old_stack)
        # print("New")
        # print(new_stack)

        # OPTION 1: Move from stack to empty
        if (old_stack and new_is_empty):
            # change top, add new top, retract ontopof, get rid of empty, change ons
            self.kb.kb_retract(Fact(Statement(["empty", new_location])))
            self.kb.kb_retract(Fact(Statement(["top", object, old_location])))
            self.kb.kb_retract(Fact(Statement(["onTopOf", object, old_stack.list_of_bindings[0][0].bindings_dict["?X"]])))
            self.kb.kb_retract(Fact(Statement(["on", object, old_location])))

            self.kb.kb_assert(Fact(Statement(["on", object, new_location])))
            self.kb.kb_assert(Fact(Statement(["top", old_stack.list_of_bindings[0][0].bindings_dict["?X"], old_location])))
            self.kb.kb_assert(Fact(Statement(["top", object, new_location])))

        # OPTION 2: Move from stack to stack
        elif (old_stack and new_stack):

            self.kb.kb_retract(Fact(Statement(["top", object, old_location])))
            self.kb.kb_retract(Fact(Statement(["onTopOf", object, old_stack.list_of_bindings[0][0].bindings_dict["?X"]])))
            self.kb.kb_retract(Fact(Statement(["top", new_stack.list_of_bindings[0][0].bindings_dict["?x"], new_location])))
            self.kb.kb_retract(Fact(Statement(["on", object, old_location])))

            self.kb.kb_assert(Fact(Statement(["on", object, new_location])))
            self.kb.kb_assert(Fact(Statement(["onTopOf", object, new_stack.list_of_bindings[0][0].bindings_dict["?x"]])))
            self.kb.kb_assert(Fact(Statement(["top", old_stack.list_of_bindings[0][0].bindings_dict["?X"], old_location])))
            self.kb.kb_assert(Fact(Statement(["top", object, new_location])))

        # OPTION 3: Move from empty to stack
        elif (new_stack):
            self.kb.kb_retract(Fact(Statement(["top", object, old_location])))
            self.kb.kb_retract(Fact(Statement(["top", new_stack.list_of_bindings[0][0].bindings_dict["?x"], new_location])))
            self.kb.kb_retract(Fact(Statement(["on", object, old_location])))

            self.kb.kb_assert(Fact(Statement(["onTopOf", object, new_stack.list_of_bindings[0][0].bindings_dict["?x"]])))
            self.kb.kb_assert(Fact(Statement(["top", object, new_location])))
            self.kb.kb_assert(Fact(Statement(["empty", old_location])))
            self.kb.kb_assert(Fact(Statement(["on", object, new_location])))


        # OPTION 4: Move from empty to empty
        else:
            self.kb.kb_retract(Fact(Statement(["top", object, old_location])))
            self.kb.kb_retract(Fact(Statement(["empty", new_location])))
            self.kb.kb_retract(Fact(Statement(["on", object, old_location])))

            self.kb.kb_assert(Fact(Statement(["top", object, new_location])))
            self.kb.kb_assert(Fact(Statement(["empty", old_location])))
            self.kb.kb_assert(Fact(Statement(["on", object, new_location])))

        self.kb.kb_retract(Fact(movable_statement))
        #
        # # for f in facts:
        # #     print(f)
        # # print('\n\n\n')
        #
        # new_location = movable_statement.terms[2]
        # object = movable_statement.terms[0]
        # old_location = movable_statement.terms[1]
        #
        # statement_new = Statement(["on", object, new_location] )
        # statement_old = Statement(["on", object, old_location] )
        #
        # # Add new ons
        # if (Fact(Statement(["on", "disk2", old_location])) in facts):
        #     added.append(Fact(Statement(["top", "disk2", old_location])))
        # elif (Fact(Statement(["on", "disk3", old_location])) in facts):
        #     added.append(Fact(Statement(["top", "disk3", old_location])))
        #
        # # Retract old empty
        # if (Fact(Statement(["empty", new_location])) in facts):
        #     # Must get rid of previous top
        #     for f in facts:
        #         if (f.statement.predicate == "top" and f.statement.terms[1] == new_location):
        #             retracted.append(f)
        #             break
        #
        # new_fact = Fact( statement_new )
        # old_fact = Fact( statement_old )
        #
        # retracted.append(old_fact)
        # added.append(new_fact)
        # # self.kb.kb_assert(new_fact)
        #
        #
        # # We know moved disk was and still is a top, simply need to switch top type
        # retracted.append(Fact(Statement(["top", object, old_location])))
        # added.append(Fact(Statement(["top", object, new_location])))
        #
        # # retract old onTopOf
        # if (Fact(Statement(["onTopOf", "disk2", object])) in facts):
        #     retracted.append(Fact(Statement(["onTopOf", "disk2", object])))
        # elif (Fact(Statement(["onTopOf", "disk3", object])) in facts):
        #     retracted.append(Fact(Statement(["onTopOf", "disk3", object])))
        #
        # if (not Fact(Statement(["empty", new_location]))):
        #     # We need to get rid of the top on it and add an onTopOf
        #     if (Fact(Statement(["on", "disk2", new_location])) in facts):
        #         retract.append(Fact(Statement(["top", "disk2", new_location])))
        #         added.append(Fact(Statement(["onTopOf", object, "disk2"])))
        #     elif (Fact(Statement(["on", "disk3", new_location])) in facts):
        #         retract.append(Fact(Statement(["top", "disk3", new_location])))
        #         added.append(Fact(Statement(["onTopOf", object, "disk3"])))
        #
        # for a in added:
        #     if ((a not in facts)):
        #         # print("Added")
        #         # print(a)
        #         self.kb.kb_assert(a)
        #
        # for r in retracted:
        #     # print("Retracted")
        #     # print(r)
        #     self.kb.kb_retract(r)
        #
        # # Assert new empties
        # states = self.getGameState()
        # for i, s in enumerate(states):
        #     if (s == ()):
        #         peg = "peg" + str(i + 1)
        #         self.kb.kb_assert(Fact(Statement(["empty", peg])))


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        tupl = [['', '', ''], ['', '', ''], ['', '', '']]
        facts = self.kb.facts

        for f in facts:
            if f.statement.predicate == "coordinate":
                if (not str(f.statement.terms[0]) == "empty"):
                    tupl[int(str(f.statement.terms[2])[3]) - 1][int(str(f.statement.terms[1])[3]) - 1] = int(str(f.statement.terms[0])[4])
                else:
                    tupl[int(str(f.statement.terms[2])[3]) - 1][int(str(f.statement.terms[1])[3]) - 1] = -1
        t = tuple([tuple(tupl[0]), tuple(tupl[1]), tuple(tupl[2])])

        return t
        pass

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

        object = movable_statement.terms[0]
        old_x_pos = movable_statement.terms[1]
        old_y_pos = movable_statement.terms[2]
        new_x_pos = movable_statement.terms[3]
        new_y_pos = movable_statement.terms[4]

        new_fact = Fact(Statement(["coordinate", object, new_x_pos, new_y_pos]))
        old_fact = Fact(Statement(["coordinate", object, old_x_pos, old_y_pos]))

        old_empty = Fact(Statement(["coordinate", "empty", new_x_pos, new_y_pos]))
        new_empty = Fact(Statement(["coordinate", "empty", old_x_pos, old_y_pos]))

        self.kb.kb_retract(old_fact)
        self.kb.kb_retract(old_empty)

        self.kb.kb_assert(new_fact)
        self.kb.kb_assert(new_empty)

        pass

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))

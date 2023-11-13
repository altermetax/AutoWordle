from .dict_loader import get_possible_words
from .wordle_util import absurdle_step, wordle_filter

class BasicAbsurdleSolver:
    def __init__(self, data_path):
        self.remaining_words = get_possible_words(data_path)

    def get_guess(self, new_game_state):
        # Restrict remaining_words based on new data
        for colored_word in new_game_state:
            self.remaining_words = wordle_filter(self.remaining_words, colored_word)

        choices = {}
        for word in self.remaining_words:
            (groups, best_answer) = absurdle_step(word, self.remaining_words)
            choices[word] = (groups, len(groups[best_answer]))

        best_user_answer = min(choices, key=lambda k : choices[k][1])

        return {
            "word": best_user_answer
        }

class Node:
    def __init__(self):
        self.picked_word = None
        self.remaining_words = None
        self.parent = None
        self.children = []
        self.depth = 0
        self._value = None

    def set_parent(self, parent):
        self.parent = parent
        parent.children.append(self)
    
    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def expand(self):
        if self.remaining_words is None:
            raise RuntimeError("Called expand when remaining_words is None")
        for word in self.remaining_words:
            new_child = Node()
            new_child.picked_word = word
            new_child.depth = self.depth + 1
            (groups, absurdle_answer) = absurdle_step(word, self.remaining_words)
            new_child.remaining_words = groups[absurdle_answer]
            self.add_child(new_child)
    
    def expand_if_childless(self):
        if len(self.children) == 0:
            self.expand()

    @property
    def value(self):
        if self._value is not None:
            return self._value
        else:
            if len(self.remaining_words) == 1:
                if self.remaining_words[0] == self.picked_word:
                    self._value = 0
                else:
                    self._value = 1
            else:
                self._value = len(self.remaining_words)
            return self._value
    
    @property
    def picks(self):
        current_node = self
        picks = []
        while current_node.parent is not None:
            picks.append(current_node.picked_word)
            current_node = current_node.parent
        picks.reverse()
        return picks

    @property
    def first_pick(self):
        picks = self.picks
        if len(picks) == 0:
            return None
        else:
            return picks[0]

    def __str__(self):
        picks = self.picks
        if len(picks) == 0:
            return "Empty Node"
        out = ""
        for pick in picks:
            out += pick + " → "
        return out[:-3]



class AbsurdleSolver:
    def __init__(self, data_path):
        self.maxdepth = 8
        self.number_of_past_attempts = 0
        self.remaining_words = get_possible_words(data_path)

    def get_guess(self, new_game_state):
        # Restrict remaining_words based on new data
        for colored_word in new_game_state:
            self.remaining_words = wordle_filter(self.remaining_words, colored_word)

        self.number_of_past_attempts += len(new_game_state)
        
        root = Node()
        root.remaining_words = self.remaining_words
        root.depth = 0

        if self.number_of_past_attempts == 0:
            #solution_node = self.find_solution_depth_first(root, self.maxdepth)
            best_user_answer = "AGILE"
        else:
            solution_node = self.find_solution_iterative_deepening(root, self.maxdepth)
            if solution_node is None:
                best_user_answer = None
            else:
                best_user_answer = solution_node.first_pick

        return {
            "word": best_user_answer
        }

    def find_solution_breadth_first(self, root, maxdepth):
        best_solution = None
        fringe = [root]

        while True:
            if len(fringe) == 0:
                return best_solution

            node = fringe.pop(0) # pop from start of fringe
            print("Checking", node, "depth=" + str(node.depth), "value=" + str(node.value))

            if node.depth > maxdepth:
                return None

            if node.value == 0:
                return node # Node is optimal solution
            elif best_solution is None or node.value > best_solution.value:
                best_solution = node # Node is a better solution than the previous best one

            node.expand()
            fringe += node.children

    def find_solution_depth_first(self, root, maxdepth):
        fringe = [root]

        while True:
            if len(fringe) == 0:
                return None # max_depth was too small for a solution

            node = fringe.pop() # pop from end of fringe
            print("Checking", node, "depth=" + str(node.depth), "value=" + str(node.value))

            if node.value == 0:
                return node # Node is optimal solution
            #elif best_solution is None or node.value > best_solution.value:
            #    best_solution = node # Node is a better solution than the previous best one

            if node.depth < maxdepth:
                node.expand_if_childless()
                fringe += node.children

    def find_solution_iterative_deepening(self, root, maxdepth):
        for depth in range(maxdepth + 1):
            solution = self.find_solution_depth_first(root, depth)
            if solution is not None:
                return solution
        print("No solution found")
        return None

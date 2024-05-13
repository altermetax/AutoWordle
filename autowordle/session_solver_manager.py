from .wordle_solver import WordleSolver
from .absurdle_solver import AbsurdleSolver

class SessionSolverManager:
    solvers = {}
    next_id = 0

    def new_solver(self, type, data_path):
        id = self.next_id
        self.next_id += 1

        if type == "wordle":
            self.solvers[id] = WordleSolver(data_path)
        elif type == "absurdle":
            self.solvers[id] = AbsurdleSolver(data_path)

        return id

    def get_guess(self, solver_id, new_game_state):
        if solver_id not in self.solvers:
            return None
        game = self.solvers[solver_id]
        return game.get_guess(new_game_state)

from autowordle.wordle_solver import WordleSolver, SandersonWordleSolver
from autowordle.absurdle_solver import AbsurdleSolver, BasicAbsurdleSolver
from autowordle.dict_loader import get_possible_words
from autowordle.wordle import Wordle

# Run the provided solver on all possible Wordle solutions
def run(data_path, solver_class):
    solutions = get_possible_words(data_path)
    attempt_counts = {}
    
    for solution in solutions:
        results = test_solution(data_path, solver_class, solution)
        if results["ok"]:
            n_attempts = len(results["game"])
            print(f"Solution {solution}: {n_attempts} attempts")
            if n_attempts in attempt_counts:
                attempt_counts[n_attempts] += 1
            else:
                attempt_counts[n_attempts] = 1
            print(attempt_counts)
        else:
            print(f"Solution {solution}: {results['msg']}")

    numerator = 0
    denominator = 0
    for n_attempts, n_instances in attempt_counts.items():
        numerator += n_attempts * n_instances
        denominator += n_instances

    average_n_attempts = numerator / denominator
    print(f"Number of attempts on average: {average_n_attempts}")
        
# Run the provided solver with the provided game on the provided solution
def test_solution(data_path, solver_class, solution):
    wordle = Wordle(data_path, False, solution)
    solver = solver_class(data_path, verbose=False)

    game = []
    new_game_state = []
    while True:
        guess = solver.get_guess(new_game_state)["word"]
        if guess is None:
            return {
                "ok": False,
                "msg": "failed"
            }
        result = wordle.try_word(guess)
        if not result["valid"]:
            return {
                "ok": False,
                "msg": "used invalid word: {guess}"
            }
        
        new_game_state = [[]]
        for i in range(len(guess)):
            new_game_state[0].append({"letter": guess[i], "color": result["result"][i]})
        
        game.append(new_game_state[0])
        
        green_count = 0
        for c in result["result"]:
            if c == "green":
                green_count += 1
        if green_count == 5:
            break

    return {
        "ok": True,
        "game": game
    }

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        data_path = "."
    elif len(sys.argv) == 2:
        data_path = sys.argv[1]
    else:
        print(f"{sys.argv[0]}: please use either one or zero arguments.", file=sys.stderr)
        print(f"Usage: {sys.argv[0]} [data_path]", file=sys.stderr)
        print(f"where data_path is the path to a directory containing accepted_words.txt and possible_words.txt", file=sys.stderr)
        sys.exit(1)

    run(data_path, AbsurdleSolver)

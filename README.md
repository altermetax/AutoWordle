# AutoWordle

AutoWordle is a Wordle and Absurdle clone with a Flask-based web interface and an integrated “autopilot” feature that can be enabled or disabled during a game which makes attempts based on artificial intelligence algorithms.

## Wordle Algorithms

To solve Wordle, two algorithms can be used: `StatisticalWordleSolver` and `SandersonWordleSolver`. `StatisticalWordleSolver` relies on statistics, while `SandersonWordleSolver` is based on information theory and is an implementation of the algorithm showcased by YouTuber Grant Sanderson in his video [Solving Wordle Using Information Theory](https://www.youtube.com/watch?v=v68zYyaEmEA).

Both algorithms perform similarly, but the second one is slightly better.

## Absurdle Algorithms

Two separate algorithms are included to solve Absurdle: `BasicAbsurdleSolver` and `TreeAbsurdleSolver`. `BasicAbsurdleSolver` simply makes the choice most convenient to the player by checking all possible words, while `TreeAbsurdleSolver` is a tree search algorithm which finds the solution closest to the current point in the game.

## Performance

Testing with all possible Wordle answers:

| Number of required attempts | `StatisticalWordleSolver` | `SandersonWordleSolver` | `BasicAbsurdleSolver` | `TreeAbsurdleSolver` |
|-----------------------------|---------------------------|-------------------------|-----------------------|----------------------|
| 1                           | 1                         | 1                       | 1                     | 0                    |
| 2                           | 131                       | 131                     | 122                   | 145                  |
| 3                           | 983                       | 986                     | 880                   | 783                  |
| 4                           | 920                       | 925                     | 1012                  | 1069                 |
| 5                           | 220                       | 211                     | 235                   | 303                  |
| 6                           | 44                        | 45                      | 47                    | 9                    |
| 7                           | 10                        | 10                      | 11                    | 2                    |
| 8                           | 2                         | 2                       | 3                     | 0                    |
| Average number of attempts  | 3.6097                    | 3.6054                  | 3.6742                | 3.6772               |

Required attempts to solve Absurdle:

- `StatisticalWordleSolver`: 6
- `SandersonWordleSolver`: 6
- `BasicAbsurdleSolver`: 5
- `TreeAbsurdleSolver`: 4

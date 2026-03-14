import sys
import re
import argparse
from solvability import is_solvable
from astar import astar, idastar
from heuristiques import manhattan, hamming, linear_conflict, zero_heuristic

HEURISTICS = {
    "manhattan": manhattan,
    "hamming":   hamming,
    "linear":    linear_conflict,
}

MODES = {
    "astar":   "A* (g + h)",
    "greedy":  "Greedy Best-First (h only)",
    "uniform": "Uniform Cost Search (g only)",
}

def parse_file(filename):
    try:
        try:
            with open(filename, 'r', encoding='utf-8-sig') as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            with open(filename, 'r', encoding='utf-16') as f:
                lines = f.readlines()

        clean_lines = []
        for line in lines:
            line = re.sub(r'#.*', '', line).strip()
            if line:
                clean_lines.append(line)

        if not clean_lines:
            raise ValueError("Empty or invalid file.")

        size = int(clean_lines[0])
        board = []
        for row in clean_lines[1:size + 1]:
            numbers = list(map(int, row.split()))
            if len(numbers) != size:
                raise ValueError(f"Row has {len(numbers)} numbers, expected {size}.")
            board.append(numbers)

        if len(board) != size:
            raise ValueError(f"Board has {len(board)} rows, expected {size}.")

        expected = set(range(size * size))
        actual   = set(num for row in board for num in row)
        if actual != expected:
            raise ValueError(f"Invalid numbers. Expected 0-{size*size-1}.")

        return size, tuple(tuple(row) for row in board)

    except Exception as e:
        print(f"Error parsing file: {e}")
        sys.exit(1)


def print_board(tiles, size):
    w = len(str(size * size))
    for i in range(size):
        print(" ".join(str(x).rjust(w) for x in tiles[i*size:(i+1)*size]))
    print()


def main():
    parser = argparse.ArgumentParser(description="N-Puzzle Solver using A* / IDA*")
    parser.add_argument("file", help="Path to the puzzle file")
    parser.add_argument(
        "-f", "--function",
        choices=HEURISTICS.keys(),
        default="linear",
        help="Heuristic: manhattan, hamming, linear (default: linear)"
    )
    parser.add_argument(
        "-m", "--mode",
        choices=MODES.keys(),
        default="astar",
        help="Search mode: astar, greedy, uniform (default: astar)"
    )
    args = parser.parse_args()


    if args.mode == "uniform":
        heuristic_fn   = zero_heuristic
        heuristic_name = "zero (uniform cost)"
    else:
        heuristic_fn   = HEURISTICS[args.function]
        heuristic_name = args.function

  
    size, board = parse_file(args.file)
    start_tiles = tuple(num for row in board for num in row)

    print(f"Puzzle Size  : {size}x{size}")
    print("\nInitial State:")
    print_board(start_tiles, size)


    solvable, goal = is_solvable(board, size)
    if not solvable:
        print("This puzzle is unsolvable.")
        sys.exit(0)

    goal_tiles = tuple(num for row in goal for num in row)

    print("Goal State:")
    print_board(goal_tiles, size)

    print(f"Heuristic    : {heuristic_name}")
    print(f"Mode         : {MODES[args.mode]}")


    if size <= 3 or args.mode != "astar": 
        print("Algorithm    : A*\n")
        path, time_c, space_c = astar(start_tiles, goal_tiles, size,
                                       heuristic_fn, mode=args.mode)
    else:
        print("Algorithm    : IDA*\n")
        path, time_c, space_c = idastar(start_tiles, goal_tiles, size,
                                         heuristic_fn, mode=args.mode)


    if path is None:
        print("No solution found.")
        sys.exit(1)

    print(f"Time complexity  : {time_c} states selected")
    print(f"Space complexity : {space_c} states in memory")
    print(f"Number of moves  : {len(path) - 1}")
    print("\nSolution path:")
    for state in path:
        print_board(state.tiles, size)


if __name__ == "__main__":
    main()
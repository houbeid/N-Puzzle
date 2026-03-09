# main.py
import sys
import re
import argparse
import random
from solvability import is_solvable, make_goal
from astar import astar, idastar
from heuristiques import manhattan, hamming, linear_conflict

HEURISTICS = {
    "manhattan": manhattan,
    "hamming":   hamming,
    "linear":    linear_conflict,
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

        # Validation des nombres
        expected = set(range(size * size))
        actual   = set(num for row in board for num in row)
        if actual != expected:
            raise ValueError(f"Invalid numbers. Expected 0-{size*size-1}.")

        return size, tuple(tuple(row) for row in board)

    except Exception as e:
        print(f"Error parsing file: {e}")
        sys.exit(1)


def generate_random(size, iterations=10000):
    """
    Génère un puzzle solvable en partant du goal
    et en faisant des moves aléatoires valides.
    """
    def swap_empty(p):
        idx = p.index(0)
        poss = []
        if idx % size > 0:       poss.append(idx - 1)
        if idx % size < size - 1: poss.append(idx + 1)
        if idx // size > 0:       poss.append(idx - size)
        if idx // size < size - 1: poss.append(idx + size)
        swi = random.choice(poss)
        p[idx], p[swi] = p[swi], p[idx]

    # Partir du goal spirale (garanti solvable)
    goal = make_goal(size)
    p = list(num for row in goal for num in row)

    for _ in range(iterations):
        swap_empty(p)

    board = tuple(tuple(p[i*size:(i+1)*size]) for i in range(size))
    return size, board


def print_board(tiles, size):
    w = len(str(size * size))
    for i in range(size):
        print(" ".join(str(x).rjust(w) for x in tiles[i*size:(i+1)*size]))
    print()


def main():
    parser = argparse.ArgumentParser(description="N-Puzzle Solver using A* / IDA*")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("file", nargs="?", help="Path to the puzzle file")
    group.add_argument("-s", "--size", type=int, help="Generate a random puzzle of given size")

    parser.add_argument(
        "-f", "--function",
        choices=HEURISTICS.keys(),
        default="linear",
        help="Heuristic: manhattan, hamming, linear (default: linear)"
    )
    parser.add_argument(
        "-i", "--iterations",
        type=int,
        default=10000,
        help="Iterations for random generation (default: 10000)"
    )
    args = parser.parse_args()

    # 1. Parse ou génération
    if args.size:
        if args.size < 3:
            print("Error: size must be >= 3.")
            sys.exit(1)
        print(f"Generating random {args.size}x{args.size} puzzle...")
        size, board = generate_random(args.size, args.iterations)
    else:
        size, board = parse_file(args.file)

    start_tiles = tuple(num for row in board for num in row)

    print(f"Puzzle Size  : {size}x{size}")
    print("\nInitial State:")
    print_board(start_tiles, size)

    # 2. Solvability
    solvable, goal = is_solvable(board, size)
    if not solvable:
        print("This puzzle is unsolvable.")
        sys.exit(0)

    goal_tiles = tuple(num for row in goal for num in row)

    print("Goal State:")
    print_board(goal_tiles, size)

    # 3. Heuristique
    heuristic_fn = HEURISTICS[args.function]
    print(f"Heuristic    : {args.function}")

    # 4. Algo selon taille
    if size <= 3:
        print("Algorithm    : A*\n")
        path, time_c, space_c = astar(start_tiles, goal_tiles, size, heuristic_fn)
    else:
        print("Algorithm    : IDA*\n")
        path, time_c, space_c = idastar(start_tiles, goal_tiles, size, heuristic_fn)

    # 5. Résultat
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
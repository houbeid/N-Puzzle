# Makefile for N-Puzzle

NAME = n-puzzle

# Default puzzle size for random generation
SIZE = 3

# Default puzzle file
FILE = puzzle.txt

# Colors
GREEN  = \033[0;32m
YELLOW = \033[0;33m
RESET  = \033[0m

all:
	@echo "$(GREEN)N-Puzzle Solver$(RESET)"
	@echo "Usage:"
	@echo "  make run FILE=puzzle.txt        - Solve a puzzle file"
	@echo "  make gen SIZE=3                 - Generate a solvable puzzle"
	@echo "  make gen_unsolvable SIZE=3      - Generate an unsolvable puzzle"
	@echo "  make test                       - Run tests on 3x3, 4x4, 5x5"
	@echo "  make clean                      - Remove generated files"

# Run solver on a file
run:
	python main.py $(FILE)

# Run with specific heuristic
run_manhattan:
	python main.py $(FILE) -f manhattan

run_hamming:
	python main.py $(FILE) -f hamming

run_linear:
	python main.py $(FILE) -f linear

# Run with specific mode (bonus)
run_greedy:
	python main.py $(FILE) -f linear -m greedy

run_uniform:
	python main.py $(FILE) -m uniform

# Generate puzzles
gen:
	@echo "$(YELLOW)Generating solvable $(SIZE)x$(SIZE) puzzle...$(RESET)"
	python npuzzle-gen.py $(SIZE) -s > $(FILE)
	@echo "$(GREEN)Puzzle saved to $(FILE)$(RESET)"
	@cat $(FILE)

gen_unsolvable:
	@echo "$(YELLOW)Generating unsolvable $(SIZE)x$(SIZE) puzzle...$(RESET)"
	python npuzzle-gen.py $(SIZE) -u > puzzle_unsolvable.txt
	@echo "$(GREEN)Puzzle saved to puzzle_unsolvable.txt$(RESET)"
	@cat puzzle_unsolvable.txt

# Test various sizes
test:
	@echo "$(YELLOW)Testing 3x3...$(RESET)"
	python npuzzle-gen.py 3 -s > test3.txt
	python main.py test3.txt -f linear
	@echo "$(YELLOW)Testing 4x4...$(RESET)"
	python npuzzle-gen.py 4 -s -i 100 > test4.txt
	python main.py test4.txt -f linear
	@echo "$(YELLOW)Testing 5x5...$(RESET)"
	python npuzzle-gen.py 5 -s -i 50 > test5.txt
	python main.py test5.txt -f linear
	@echo "$(GREEN)All tests done!$(RESET)"

# Test unsolvable
test_unsolvable:
	@echo "$(YELLOW)Testing unsolvable puzzle...$(RESET)"
	python npuzzle-gen.py 3 -u > test_unsolvable.txt
	python main.py test_unsolvable.txt

# Clean generated files
clean:
	@rm -f test3.txt test4.txt test5.txt test_unsolvable.txt puzzle_unsolvable.txt
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -type d -exec rm -rf {} +
	@echo "$(GREEN)Cleaned!$(RESET)"

fclean: clean
	@rm -f $(FILE)

re: fclean all

.PHONY: all run run_manhattan run_hamming run_linear \
        run_greedy run_uniform gen gen_unsolvable \
        test test_unsolvable clean fclean re
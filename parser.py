import sys
import re

def parse_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8-sig') as f:
            lines = f.readlines()
        
        # Remove comments and empty lines
        clean_lines = []
        for line in lines:
            line = re.sub(r'#.*', '', line).strip()
            if line:
                clean_lines.append(line)
        
        if not clean_lines:
            raise ValueError("Empty or invalid file.")

        size = int(clean_lines[0])
        board = [[0] * size for _ in range(size)]
        for i, row in enumerate(clean_lines[1:]):
            numbers = list(map(int, row.split()))
            board[i] = numbers

        tuple_board = tuple(tuple(row) for row in board)
            
        return size, tuple_board

    except Exception as e:
        print(f"Error parsing file: {e}")
        sys.exit(1)
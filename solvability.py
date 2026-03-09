def make_goal(size):
    ts = size * size
    puzzle = [-1 for i in range(ts)]
    cur = 1
    x = 0; ix = 1
    y = 0; iy = 0
    while True:
        puzzle[x + y * size] = cur
        if cur == 0:
            break
        cur += 1
        if x + ix == size or x + ix < 0 or (ix != 0 and puzzle[x + ix + y * size] != -1):
            iy = ix; ix = 0
        elif y + iy == size or y + iy < 0 or (iy != 0 and puzzle[x + (y + iy) * size] != -1):
            ix = -iy; iy = 0
        x += ix; y += iy
        if cur == size * size:
            cur = 0
    return tuple(tuple(puzzle[i * size:(i + 1) * size]) for i in range(size))


def permutation_parity(flat_board, flat_goal):
    """
    Parité de la permutation qui transforme flat_board en flat_goal.
    """
    # On travaille uniquement sur les valeurs non-nulles
    board_vals = [x for x in flat_board if x != 0]
    goal_vals  = [x for x in flat_goal  if x != 0]

    # Position de chaque valeur dans goal (sans le 0)
    goal_index = {val: i for i, val in enumerate(goal_vals)}

    # Permutation P : pour chaque valeur dans board_vals,
    # où est-elle dans goal_vals ?
    perm = [goal_index[val] for val in board_vals]

    # Compter les cycles pour déterminer la parité
    visited = [False] * len(perm)
    parity = 0
    for i in range(len(perm)):
        if not visited[i]:
            cycle_len = 0
            j = i
            while not visited[j]:
                visited[j] = True
                j = perm[j]  # j reste toujours dans [0, len(perm)-1]
                cycle_len += 1
            parity += cycle_len - 1

    return parity % 2


def is_solvable(board, size):
    flat_board = [j for row in board for j in row]
    goal = make_goal(size)
    flat_goal = [val for row in goal for val in row]

    parity = permutation_parity(flat_board, flat_goal)

    if size % 2 == 1:
        solvable = parity == 0
    else:
        blank_board = flat_board.index(0)
        blank_goal  = flat_goal.index(0)
        row_board = blank_board // size
        row_goal  = blank_goal  // size
        solvable = (parity + row_board + row_goal) % 2 == 0

    return solvable, goal
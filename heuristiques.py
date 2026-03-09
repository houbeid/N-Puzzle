def manhattan(state, goal_pos):
    dist = 0
    for idx, val in enumerate(state.tiles):
        if val != 0:
            curr_r, curr_c = divmod(idx, state.size)
            goal_r, goal_c = goal_pos[val]
            dist += abs(curr_r - goal_r) + abs(curr_c - goal_c)
    return dist

def hamming(state, goal_pos):
    count = 0
    for idx, val in enumerate(state.tiles):
        if val != 0:
            curr_r, curr_c = divmod(idx, state.size)
            goal_r, goal_c = goal_pos[val]
            if (curr_r, curr_c) != (goal_r, goal_c):
                count += 1
    return count

def linear_conflict(state, goal_pos):
    dist = manhattan(state, goal_pos)
    conflicts = 0
    size = state.size

    # Conflits lignes
    for r in range(size):
        row_tiles = [
            (goal_pos[state.tiles[r*size+c]][1], c)
            for c in range(size)
            if state.tiles[r*size+c] != 0
            and goal_pos[state.tiles[r*size+c]][0] == r
        ]
        for i in range(len(row_tiles)):
            for j in range(i+1, len(row_tiles)):
                if (row_tiles[i][1] < row_tiles[j][1]) != (row_tiles[i][0] < row_tiles[j][0]):
                    conflicts += 1

    # Conflits colonnes
    for c in range(size):
        col_tiles = [
            (goal_pos[state.tiles[r*size+c]][0], r)
            for r in range(size)
            if state.tiles[r*size+c] != 0
            and goal_pos[state.tiles[r*size+c]][1] == c
        ]
        for i in range(len(col_tiles)):
            for j in range(i+1, len(col_tiles)):
                if (col_tiles[i][1] < col_tiles[j][1]) != (col_tiles[i][0] < col_tiles[j][0]):
                    conflicts += 1

    return dist + 2 * conflicts
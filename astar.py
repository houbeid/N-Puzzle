import heapq
import time
from PuzzleState import PuzzleState

MAX_TIME = 60

def make_goal_pos(goal_tiles, size):
    return {val: divmod(idx, size) for idx, val in enumerate(goal_tiles)}


def astar(start_tiles, goal_tiles, size, heuristic_fn):
    goal_pos   = make_goal_pos(goal_tiles, size)
    start      = PuzzleState(start_tiles, size, goal_pos, heuristic_fn=heuristic_fn)
    goal_state = PuzzleState(goal_tiles, size, goal_pos)

    open_heap = [start]
    visited   = {}

    time_complexity  = 0
    space_complexity = 0

    while open_heap:
        space_complexity = max(space_complexity, len(open_heap))
        current = heapq.heappop(open_heap)

        if current.tiles in visited and visited[current.tiles] <= current.g:
            continue
        visited[current.tiles] = current.g
        time_complexity += 1

        if current == goal_state:
            return current.reconstruct_path(), time_complexity, space_complexity

        for neighbor in current.get_neighbors(goal_pos, heuristic_fn):
            if neighbor.tiles not in visited or visited[neighbor.tiles] > neighbor.g:
                heapq.heappush(open_heap, neighbor)

    return None, time_complexity, space_complexity


def idastar(start_tiles, goal_tiles, size, heuristic_fn):
    goal_pos   = make_goal_pos(goal_tiles, size)
    start      = PuzzleState(start_tiles, size, goal_pos, heuristic_fn=heuristic_fn)
    goal_state = PuzzleState(goal_tiles, size, goal_pos)

    threshold  = start.h
    path       = [start]
    start_time = time.time()

    time_complexity  = 0
    space_complexity = 0

    def search(g, threshold):
        nonlocal time_complexity, space_complexity
        current = path[-1]
        f = g + current.h

        if f > threshold:
            return f, None
        if current == goal_state:
            return -1, list(path)

        if time.time() - start_time > MAX_TIME:
            return float('inf'), None

        time_complexity += 1
        space_complexity = max(space_complexity, len(path))

        minimum  = float('inf')
        prev_tiles = path[-2].tiles if len(path) > 1 else None

        neighbors = current.get_neighbors(goal_pos, heuristic_fn)
        neighbors.sort(key=lambda n: n.f)

        for neighbor in neighbors:
            if neighbor.tiles == prev_tiles:
                continue
            path.append(neighbor)
            t, result = search(g + 1, threshold)
            if result is not None:
                return -1, result
            if t < minimum:
                minimum = t
            path.pop()

        return minimum, None

    print(f"Initial h    : {start.h}")

    iteration = 0
    while True:
        iteration += 1
        elapsed = time.time() - start_time
        print(f"Iteration {iteration:3d} | threshold={threshold:4d} | "
              f"states={time_complexity:8d} | elapsed={elapsed:.1f}s")

        if elapsed > MAX_TIME:
            print(f"\nTimeout after {MAX_TIME}s.")
            return None, time_complexity, space_complexity

        t, result = search(0, threshold)
        if result is not None:
            return result, time_complexity, space_complexity
        if t == float('inf'):
            return None, time_complexity, space_complexity
        threshold = t
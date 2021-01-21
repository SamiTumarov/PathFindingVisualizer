EMPTY = 0 # Empty cell
WALL = 1 # wall/obstacle in the board
POINT = 2 # Endpoint in the board

def get_near(pos, board):
    max_row = len(board) - 1
    neighbors = []
    row, col = pos
    if row > 0:
        neighbors.append((row - 1, col))
    if col > 0:
        neighbors.append((row, col - 1))
    if row < max_row:
        neighbors.append((row + 1, col))
    if col < max_row:
        neighbors.append((row, col + 1))

    # Sort neighbors
    new_neighbors = []
    for neighbor in neighbors:
        row, col = neighbor
        if board[row][col] != WALL:
            new_neighbors.append(neighbor)

    return new_neighbors


def get_points(board):
    """ Find start and end points """
    endpoints = []
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == POINT:
                endpoints.append((row, col))
    return endpoints


def BFS(board):
    start, end = get_points(board)
    queue = [(start, [])]
    visited = []

    while len(queue) > 0:
        pos, path = queue.pop(0)
        path.append(pos)

        # Function is stopped, main loop updates screen and fetches
        # user input. Then the func is continued
        if pos == end:
            for point in path: # yield path when found
                yield (True, point) # true to signal
            break

        if pos != start:
            yield pos

        path.append(pos)
        visited.append(pos)

        neighbors = get_near(pos, board)
        # add to the list neighbors that the func didn't visit already
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.append(neighbor)
                queue.append((neighbor, path[:]))
    yield (False, None) # yield this when can't find path

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]

    def reset(self):
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]

    def is_valid_position(self, piece, dx=0, dy=0, rotation=None):
        for x, y in piece.cells(dx=dx, dy=dy, rotation=rotation):
            if x < 0 or x >= self.width or y >= self.height:
                return False
            if y >= 0 and self.grid[y][x] is not None:
                return False
        return True

    def lock_piece(self, piece):
        top_out = False
        for x, y in piece.cells():
            if y < 0:
                top_out = True
                continue
            self.grid[y][x] = piece.kind
        return top_out

    def clear_lines(self):
        kept_rows = [row for row in self.grid if any(cell is None for cell in row)]
        cleared = self.height - len(kept_rows)

        for _ in range(cleared):
            kept_rows.insert(0, [None for _ in range(self.width)])

        self.grid = kept_rows
        return cleared

    def hard_drop_distance(self, piece):
        distance = 0
        while self.is_valid_position(piece, dy=distance + 1):
            distance += 1
        return distance

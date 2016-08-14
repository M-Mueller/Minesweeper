"""A minesweeper game"""

import random
from table import Table

class Game:
    """Playing field of the minesweeper game.
    The game provides 4 tables:
    1. The mines table indicate if a field contains a mine
    2. The flags table holds which fields are flagged as mines
    3. The revealed table holds which fields are already revealed
    4. The hints table holds a pre-computed number of surrounding mines for
       each field
    """

    def __init__(self, mines, flags=None, revealed=None):
        """Generates a Game from a given mine configuration.
        If flags is None, it will be initialized with Unknown.
        """
        if flags is None:
            flags = Table(mines.num_columns, mines.num_rows, False)
        if revealed is None:
            revealed = Table(mines.num_columns, mines.num_rows, False)
        if mines.size() != flags.size():
            raise ValueError('Fields cannot have different sizes ({0} != {1})'
                             .format(mines.size(), flags.size()))
        self.mines = mines
        self.flags = flags
        self.revealed = revealed
        self.hints = Table(mines.num_columns, mines.num_rows, 0)

        for i, _ in enumerate(self.hints):
            self.hints[i] = self.hint(*self.hints.linear_to_subscript(i))

    def row_count(self):
        """Returns the vertical size of the field."""
        return self.mines.num_rows

    def column_count(self):
        """Returns the horizontal size of the field."""
        return self.mines.num_columns

    def hint(self, x, y):
        """Computes and returns the number of mines in the neighboring fields
        or -1 if the field itself is a mine."""
        if self.mines[x, y]:
            return -1
        else:
            h = 0
            for a, b in self.mines.neighbors(x, y):
                if(self.mines[a, b]):
                    h += 1
            return h

    def is_solved(self):
        """Returns true if all mines are flagged."""
        for m, f in zip(self.mines, self.flags):
            # if any mine is not marked, the game is not solved
            if m and not f:
                return False
        return True

    def is_lost(self):
        """Returns true if a mine is revealed and the game is lost."""
        for m, r in zip(self.mines, self.revealed):
            if m and r:
                return True
        return False

    def auto_mark(self):
        """Marks all mines and reveals all fields but only if all non-mine
        fields are already revealed.
        """
        for m, r in zip(self.mines, self.revealed):
            # check if all non-mine fields are revealed
            if not m and not r:
                return False

        # mark all mines and reveal remaining flields
        for i, m in enumerate(self.mines):
            if m:
                self.flags[i] = True
            self.revealed[i] = True

    def reveal_all(self):
        """Reveals all fields that are not marked."""
        for i, _ in enumerate(self.revealed):
            self.revealed[i] = True

    def reveal(self, x, y, reveal_known=True):
        """Reveals a fields.
        Returns False if the revealed field was a mine field, True otherwise.
        If the revealed field has no neighboring mines all neighboring fields
        are revealed recursively.
        Revealing a Marked field resets it to Unknown again.
        If reveal_known is set, the field is already revealed and the number of
        flagged neighbors is equal to the hint, all non-flagged fields around
        the field are revealed as well.
        """
        if self.flags[x, y]:
            self.flags[x, y] = False
            return True
        elif self.revealed[x, y]:
            if self.hints[x, y] <= 0 or not reveal_known:
                return True
            self.reveal_neighbors(x, y)
        else:
            self.revealed[x, y] = True
            if self.mines[x, y]:
                return False
            else:
                if self.hint(x, y) == 0:
                    for nx, ny in self.mines.neighbors(x, y):
                        if not self.revealed[nx, ny]:
                            ok = self.reveal(nx, ny, reveal_known=False)
                            assert ok  # must not be surrounded by any mines
                self.auto_mark()
        return True

    def reveal_neighbors(self, x, y):
        neighbors = list(self.mines.neighbors(x, y))
        neighbor_flagged_mines = [
            (nx, ny) for nx, ny in neighbors if self.flags[nx, ny]]
        if len(neighbor_flagged_mines) == self.hints[x, y]:
            for nx, ny in neighbors:
                if (nx, ny) not in neighbor_flagged_mines:
                    # don't reveal fields recursively
                    self.reveal(nx, ny, reveal_known=False)

    def toggle_mark(self, x, y):
        """Toggles the mark of a field.
        Does nothing on already revealed fields.
        """
        if not self.revealed[x, y]:
            self.flags[x, y] = not self.flags[x, y]
            self.auto_mark()

    def print_field(self):
        s = ''
        for y in range(self.mines.num_rows):
            for x in range(self.mines.num_columns):
                r, f, m = self.revealed[x, y], self.flags[x, y], self.mines[x, y]
                if not r:
                    if not f:
                        s += '?'
                    else:
                        s += '!'
                else:
                    if m:
                        if f:
                            s += "&"
                        else:
                            s += '*'
                    else:
                        if f:
                            s += "x"
                        else:
                            s += str(self.hint(x, y))
            s += '\n'
        print(s)

    @classmethod
    def create_random(cls, columns, rows, number_of_mines):
        """Generates a Grid of variable size and a specific number of
        randomly placed mines.
        """
        mines = Table(columns, rows, False)

        # indices of all fields
        fields = [(c, r) for c in range(columns) for r in range(rows)]
        # pick numMines random indices from the grid and assign them as mines
        for x, y in random.sample(fields, number_of_mines):
            mines[x, y] = True
        return Game(mines)

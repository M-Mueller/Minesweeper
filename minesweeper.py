"""A minesweeper game"""

import random
from table import table

class Flags:
    Unknown = 0
    Marked = 1
    Revealed = 2

class Game:
    """Playing field of the minesweeper game."""
    def __init__(self, mines, flags=None):
        """Generates a Grid of variable size and a specific number of mines."""
        if flags is None:
            flags = table(mines.num_columns, mines.num_rows, Flags.Unknown)
        if mines.size() != flags.size():
            raise ValueError('Fields cannot have different sizes ({0} != {1})'.format(mines.size(), flags.size()))
        self.mines = mines
        self.flags = flags
        self.hints = table(mines.num_columns, mines.num_rows, 0)

        for i, _ in enumerate(self.hints):
            self.hints[i] = self.hint(*self.hints.linear_to_subscript(i))

    def row_count(self):
        return self.mines.num_rows

    def column_count(self):
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
            if m and f != Flags.Marked:
                return False
        return True

    def is_lost(self):
        """Returns true if a mine is revealed and the game is lost."""
        for m, f in zip(self.mines, self.flags):
            if m and f == Flags.Revealed:
                return True
        return False

    def auto_mark(self):
        """Marks all mines and reveals all fields but only if all non-mine fields are already revealed."""
        for m, f in zip(self.mines, self.flags):
            # check if all non-mine fields are revealed
            if not m and f != Flags.Revealed:
                return False

        # mark all mines and reveal remaining flields
        for i, m in enumerate(self.mines):
            if m:
                self.flags[i] = Flags.Marked
            else:
                self.flags[i] = Flags.Revealed

    def reveal_all(self):
        """Reveals all fields that are not marked."""
        for i, f in enumerate(self.flags):
            if f != Flags.Marked:
                self.flags[i] = Flags.Revealed

    def reveal(self, x, y, reveal_known=True):
        """Reveals a fields.
        Returns False if the revealed field was a mine field or True otherwise.
        If the revealed field has no neighboring mines all neighboring fields are revealed recursively.
        Revealing a flagged field with reset it to unknown again.
        If reveal_known is set, the field is already revealed and the number of
        flagged neighbors is equal to the hint, all non-flagged fields around
        the field are revealed as well.
        """
        if self.flags[x, y] == Flags.Marked:
            self.flags[x, y] = Flags.Unknown
        elif self.flags[x, y] == Flags.Revealed:
            if self.hints[x, y] <= 0 or not reveal_known:
                return True
            neighbors = list(self.mines.neighbors(x, y))
            neighbor_mines = [(nx, ny) for nx, ny in neighbors if self.flags[nx, ny] == Flags.Marked]
            if len(neighbor_mines) == self.hints[x, y]:
                for nx, ny in neighbors:
                    if (nx, ny) not in neighbor_mines:
                        # don't reveal fields recursively
                        self.reveal(nx, ny, reveal_known=False)
        else:
            self.flags[x, y] = Flags.Revealed
            if self.mines[x, y]:
                return False
            else:
                if self.hint(x, y) == 0:
                    for nx, ny in self.mines.neighbors(x, y):
                        if self.flags[nx, ny] == Flags.Unknown:
                            ok = self.reveal(nx, ny, reveal_known=False)
                            assert ok # must not be surrounded by any mines
                self.auto_mark()
        return True

    def toggle_mark(self, x, y):
        """Toggles the mark of a field.
        If the field is Unknown it becomes Marked and vice versa.
        Does nothing on Revealed fields.
        """
        if self.flags[x, y] == Flags.Unknown:
            self.flags[x, y] = Flags.Marked
        elif self.flags[x, y] == Flags.Marked:
            self.flags[x, y] = Flags.Unknown
        self.auto_mark()

    def print_field(self):
        s = ''
        for y in range(self.mines.num_rows):
            for x in range(self.mines.num_columns):
                f, m = self.flags[x, y], self.mines[x, y]
                if f == Flags.Unknown:
                    s += '?'
                elif f == Flags.Marked:
                    s += '!'
                elif f == Flags.Revealed:
                    if m:
                        s += '*'
                    else:
                        s += str(self.hint(x, y))
            s += '\n'
        print(s)

    @classmethod
    def create_random(cls, columns, rows, number_of_mines):
        """Generates a Grid of variable size and a specific number of randomly placed mines."""
        mines = table(columns, rows, False)
        flags = table(columns, rows, Flags.Unknown)

        # indices of all fields
        fields = [(c, r) for c in range(columns) for r in range(rows)]
        # pick numMines random indices from the grid and assign them as mines
        for x, y in random.sample(fields, number_of_mines):
            mines[x, y] = True
        return Game(mines, flags)

if __name__ == '__main__':
    game = Game.create_random(5, 5, 2)

    while True:
        game.print_field()
        print("Select (Column, Row): ")
        try:
            x, y = map(int, input().split(','))
        except KeyboardInterrupt:
            print()
            break
        except:
            print("Invalid input")
            continue

        if not game.reveal(x, y):
            print("You Lose!")
            game.print_field()
            break
        if game.is_solved():
            print("You Win!")
            game.print_field()
            break

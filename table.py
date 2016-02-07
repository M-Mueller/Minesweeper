"""Provides a 2D table of values"""

import itertools

class Table:
    """2D table of values with m columns and n rows.
    >>> Table(2, 2)
    Table 2x2:
    [0, 0]
    [0, 0]
    >>> Table(2, 2, 1)
    Table 2x2:
    [1, 1]
    [1, 1]
    >>> Table(3, 2)
    Table 3x2:
    [0, 0, 0]
    [0, 0, 0]
    >>> Table(2, 3)
    Table 2x3:
    [0, 0]
    [0, 0]
    [0, 0]
    >>> Table(2,0)
    Traceback (most recent call last):
    ...
    ValueError: Table size cannot be smaller than 1
    >>> Table(1,-1)
    Traceback (most recent call last):
    ...
    ValueError: Table size cannot be smaller than 1
    >>> t = Table(3, 4)
    >>> t.num_rows
    4
    >>> t.num_columns
    3
    """
    def __init__(self, columns, rows, initial=0):
        if columns <= 0 or rows <= 0:
            raise ValueError('Table size cannot be smaller than 1')
        self.table = [initial for c in range(columns*rows)]
        self.num_columns = columns
        self.num_rows = rows

    def size(self):
        """Returns the dimensions of the table as a tuple."""
        return (self.num_columns, self.num_rows)

    def __getitem__(self, key):
        """Returns value of a cell.
        Key can either be a tuple of (row, column) or a linear index (i.e. column + row*num_columns).
        >>> t = Table.from_nested_list([[0, 1, 2], [3, 4, 5]])
        >>> t[0, 0]
        0
        >>> t[1,1]
        4
        >>> t[2,0]
        2
        >>> t[0,1]
        3
        >>> t[3,0]
        Traceback (most recent call last):
        ...
        IndexError: list index out of range
        >>> t[0,2]
        Traceback (most recent call last):
        ...
        IndexError: list index out of range
        >>> t[0,-1]
        3
        >>> t[0]
        0
        >>> t[5]
        5
        """
        if isinstance(key, slice):
            raise TypeError("Slicing is not supported")
        else:
            try:
                x, y = key
                if x >= self.num_columns or y >= self.num_rows:
                    raise IndexError('list index out of range')
                return self.table[self.subscript_to_linear(x, y)]
            except TypeError:
                return self.table[key]

    def __setitem__(self, key, value):
        """Overrides the value of a cell.
        Key can either be a tuple of (row, column) or a linear index (i.e. column + row*num_columns).
        >>> t = Table(3, 2)
        >>> t[0, 0] = 4
        >>> t[1, 0] = 5
        >>> t[0, 1] = 6
        >>> t
        Table 3x2:
        [4, 5, 0]
        [6, 0, 0]
        >>> t[4, 0] = 1
        Traceback (most recent call last):
        ...
        IndexError: list index out of range
        >>> t[4] = 1
        >>> t
        Table 3x2:
        [4, 5, 0]
        [6, 1, 0]
        """
        if isinstance(key, slice):
            raise TypeError("Slicing is not supported")
        else:
            try:
                x, y = key
                if x >= self.num_columns or y >= self.num_rows:
                    raise IndexError('list index out of range')
                self.table[self.subscript_to_linear(x, y)] = value
            except TypeError:
                self.table[key] = value

    def neighbors(self, x, y):
        """Returns a generator for all direct neighbors of a cell.
        Does not return the cell itself.
        Does not generate points outside the table for cells at the border.
        """
        for c in range(max(x-1, 0), min(x+2, self.num_columns)):
            for r in range(max(y-1, 0), min(y+2, self.num_rows)):
                if c != x or r != y:
                    yield (c, r)

    def linear_to_subscript(self, index):
        """Converts a linear index to a supscript index of (column, row)."""
        return (index % self.num_columns, index // self.num_columns)

    def subscript_to_linear(self, column, row):
        """Converts a supscript index (column, row) to a linear index."""
        return column + row*self.num_columns

    def count(self, value):
        """Returns the number of occurrences of value in the table."""
        return self.table.count(value)

    def row(self, r):
        """Returns a row as a list.
        >>> t = Table.from_nested_list([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]])
        >>> t.row(0)
        [0, 1, 2, 3]
        >>> t.row(2)
        [8, 9, 10, 11]
        """
        row_start = self.subscript_to_linear(0, r)
        return self.table[row_start:row_start+self.num_columns]

    def __eq__(self, other):
        """Returns true if other table has the same dimensions and content."""
        try:
            return (
                self.num_columns == other.num_columns and
                self.num_rows == other.num_rows and
                self.table == other.table
            )
        except AttributeError:
            return False

    def __repr__(self):
        """Returns the table as a string.
        >>> Table.from_nested_list([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]])
        Table 4x3:
        [0, 1, 2, 3]
        [4, 5, 6, 7]
        [8, 9, 10, 11]
        """
        s = 'Table {0}x{1}:\n'.format(self.num_columns, self.num_rows)
        for r in range(self.num_rows):
            s += repr(self.row(r)) + '\n'
        return s[:-1] #remove last newline

    def __iter__(self):
        """Iterates the table in a column major order.
        >>> t = Table.from_nested_list([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]])
        >>> [c for c in t]
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        """
        for y in range(self.num_rows):
            for x in range(self.num_columns):
                yield self[x,y]

    @classmethod
    def from_nested_list(cls, list_of_list):
        """
        >>> t = Table.from_nested_list([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]])
        >>> t.num_columns
        4
        >>> t.num_rows
        3
        >>> t
        Table 4x3:
        [0, 1, 2, 3]
        [4, 5, 6, 7]
        [8, 9, 10, 11]
        """
        # check if all internal list have the same length
        if len(set([len(l) for l in list_of_list])) > 1:
            raise ValueError('Rows cannot have different length')

        t = Table(len(list_of_list[0]), len(list_of_list))
        t.table = list(itertools.chain(*list_of_list))
        return t

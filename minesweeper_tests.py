import unittest
from table import Table
from minesweeper import Game, Flags

class MinesweeperTest(unittest.TestCase):
    def setUp(self):
        self.mines = Table.from_nested_list([
            [False, False, False, False],
            [False, True, False, False],
            [False, False, False, False],
            [False, False, False, False],
        ])
        self.flags = Table.from_nested_list([
            [Flags.Unknown, Flags.Unknown, Flags.Unknown, Flags.Unknown],
            [Flags.Unknown, Flags.Unknown, Flags.Unknown, Flags.Unknown],
            [Flags.Unknown, Flags.Unknown, Flags.Unknown, Flags.Unknown],
            [Flags.Unknown, Flags.Unknown, Flags.Unknown, Flags.Unknown],
        ])

    def test_reveal_hint(self):
        game = Game(self.mines, self.flags)
        self.assertEqual(True, game.reveal(0, 0))
        self.assertEqual(self.flags, Table.from_nested_list([
            [Flags.Revealed, Flags.Unknown, Flags.Unknown, Flags.Unknown],
            [Flags.Unknown, Flags.Unknown, Flags.Unknown, Flags.Unknown],
            [Flags.Unknown, Flags.Unknown, Flags.Unknown, Flags.Unknown],
            [Flags.Unknown, Flags.Unknown, Flags.Unknown, Flags.Unknown],
        ]))

    def test_reveal_mine(self):
        game = Game(self.mines, self.flags)
        self.assertEqual(False, game.reveal(1, 1))
        self.assertEqual(self.flags, Table.from_nested_list([
            [Flags.Unknown, Flags.Unknown, Flags.Unknown, Flags.Unknown],
            [Flags.Unknown, Flags.Revealed, Flags.Unknown, Flags.Unknown],
            [Flags.Unknown, Flags.Unknown, Flags.Unknown, Flags.Unknown],
            [Flags.Unknown, Flags.Unknown, Flags.Unknown, Flags.Unknown],
        ]))

    def test_reveal_empty(self):
        game = Game(self.mines, self.flags)
        self.assertEqual(True, game.reveal(3, 3))
        self.assertEqual(self.flags, Table.from_nested_list([
            [Flags.Unknown, Flags.Unknown, Flags.Revealed, Flags.Revealed],
            [Flags.Unknown, Flags.Unknown, Flags.Revealed, Flags.Revealed],
            [Flags.Revealed, Flags.Revealed, Flags.Revealed, Flags.Revealed],
            [Flags.Revealed, Flags.Revealed, Flags.Revealed, Flags.Revealed],
        ]))

    def test_reveal_revealed(self):
        self.flags = Table.from_nested_list([
            [Flags.Revealed, Flags.Unknown, Flags.Unknown, Flags.Unknown],
            [Flags.Unknown, Flags.Unknown, Flags.Unknown, Flags.Unknown],
            [Flags.Unknown, Flags.Unknown, Flags.Unknown, Flags.Unknown],
            [Flags.Unknown, Flags.Unknown, Flags.Unknown, Flags.Unknown],
        ])
        game = Game(self.mines, self.flags)
        self.assertEqual(True, game.reveal(0, 0))
        self.assertEqual(self.flags, Table.from_nested_list([
            [Flags.Revealed, Flags.Unknown, Flags.Unknown, Flags.Unknown],
            [Flags.Unknown, Flags.Unknown, Flags.Unknown, Flags.Unknown],
            [Flags.Unknown, Flags.Unknown, Flags.Unknown, Flags.Unknown],
            [Flags.Unknown, Flags.Unknown, Flags.Unknown, Flags.Unknown],
        ]))

    def test_reveal_marked(self):
        self.flags = Table.from_nested_list([
            [Flags.Unknown, Flags.Unknown, Flags.Unknown, Flags.Unknown],
            [Flags.Unknown, Flags.Marked, Flags.Unknown, Flags.Unknown],
            [Flags.Unknown, Flags.Unknown, Flags.Unknown, Flags.Unknown],
            [Flags.Unknown, Flags.Unknown, Flags.Unknown, Flags.Unknown],
        ])
        game = Game(self.mines, self.flags)
        self.assertEqual(True, game.reveal(1, 1))
        self.assertEqual(self.flags, Table.from_nested_list([
            [Flags.Unknown, Flags.Unknown, Flags.Unknown, Flags.Unknown],
            [Flags.Unknown, Flags.Unknown, Flags.Unknown, Flags.Unknown],
            [Flags.Unknown, Flags.Unknown, Flags.Unknown, Flags.Unknown],
            [Flags.Unknown, Flags.Unknown, Flags.Unknown, Flags.Unknown],
        ]))

    def test_reveal_revealed_hint(self):
        self.flags = Table.from_nested_list([
            [Flags.Revealed, Flags.Unknown, Flags.Unknown, Flags.Unknown],
            [Flags.Unknown, Flags.Marked, Flags.Unknown, Flags.Unknown],
            [Flags.Unknown, Flags.Unknown, Flags.Unknown, Flags.Unknown],
            [Flags.Unknown, Flags.Unknown, Flags.Unknown, Flags.Unknown],
        ])
        game = Game(self.mines, self.flags)
        self.assertEqual(True, game.reveal(0, 0))
        self.assertEqual(self.flags, Table.from_nested_list([
            [Flags.Revealed, Flags.Revealed, Flags.Unknown, Flags.Unknown],
            [Flags.Revealed, Flags.Marked, Flags.Unknown, Flags.Unknown],
            [Flags.Unknown, Flags.Unknown, Flags.Unknown, Flags.Unknown],
            [Flags.Unknown, Flags.Unknown, Flags.Unknown, Flags.Unknown],
        ]))

if __name__ == '__main__':
    unittest.main()

from table import Table
from enum import Enum

class Flags(Enum):
	Empty = 0
	Filled = 1
	Excluded = 2

class Game:
	def __init__(self, binary_picture, flags=None):
		self.fields = binary_picture
		if flags is None:
			flags = Table(self.fields.num_columns, self.fields.num_rows, Flags.Empty)
		self.flags = flags

	@classmethod
	def load(cls, path):
		with open(path, 'r') as f:
			lines = f.readlines()
		# remove trailing newline
		lines = [l.strip() for l in lines]
		fields = [[bool(int(c)) for c in l] for l in lines]
		return Game(Table.from_nested_list(fields))

	def _hints(self, fields):
		hints = []
		count = 0
		for value in fields:
			if value:
				count += 1
			else:
				if count > 0:
					hints.append(count)
					count = 0
		if count > 0:
			hints.append(count)
		if len(hints) == 0:
			hints.append(0)
		return hints	
	
	def row_hints(self, row):
		return self._hints(self.fields.row(row))
	
	def column_hints(self, column):
		return self._hints(self.fields.column(column))

	def fill(self, column, row):
		self.flags[column, row] = Flags.Filled
		return self.fields[column, row]

	def exclude(self, column, row):
		self.flags[column, row] = Flags.Exluded
		return not self.fields[column, row]

	def clear(self, column, row):
		self.flags[column, row] = Flags.Empty

	def __repr__(self):
		row_hints = [self.row_hints(r) for r in range(self.fields.num_rows)]
		max_row_hints = max(map(len, row_hints))
		column_hints = [self.column_hints(c) for c in range(self.fields.num_columns)]
		max_column_hints = max(map(len, column_hints))
		s = ''
		for c in reversed(range(max_column_hints)):
			s += ' ' * max_row_hints * 2
			for hint in column_hints:
				if c < len(hint):
					s += str(hint[c])
				else:
					s += ' '
			s += '\n'

		for row, hint in enumerate(row_hints):
			# make each lines the same length by filling with space
			s += ' ' * max(0, (max_row_hints - len(hint))*2)
			s += ' '.join(map(str, hint))
			s += ' '
			def convert(field, flag):
				if flag == Flags.Empty:
					if field:
						return '.'
					else:
						return ' '
				elif flag == Flags.Filled:
					if field:
						return '#'
					else:
						return '@'
				else:
					if field:
						return '%'
					else:
						return 'X'
			fields = [convert(a, b) for a,b in zip(self.fields.row(row), self.flags.row(row))]
			s += ''.join(fields)
			s += '\n'
		return s

if __name__ == '__main__':
	for p in ['arrow.pic', 'box.pic']:
		game = Game.load(p)
		print(game)

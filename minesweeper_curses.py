"""Curses interface for minesweeper"""

import curses
import os
from collections import namedtuple
import minesweeper

class Rect:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __repr__(self):
        return "({0}, {1}, {2}, {3})".format(self.x, self.y, self.width, self.height)

def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)

def draw_frame(stdscr, rect, thick_border=False):
    """Draws a frame in an rectangular area."""
    if thick_border:
        template = [["\u2554", "\u2550", "\u2557"],
            ["\u2551", " ", "\u2551"],
            ["\u255A", "\u2550", "\u255D"]
        ]
    else:
        template = [["\u250C", "\u2500", "\u2510"],
            ["\u2502", " ", "\u2502"],
            ["\u2514", "\u2500", "\u2518"]
        ]

    for h in range(rect.height):
        if h == 0:
            k = 0
        elif h < rect.height-1:
            k = 1
        else:
            k = 2
        line = template[k][0] + (rect.width-2)*template[k][1] + template[k][2]
        stdscr.addstr(rect.y+h, rect.x, line)
    return Rect(rect.x+1, rect.y+1, rect.width-2, rect.height-2)

def draw_game(stdscr, rect, game):
    """Draws the game fields."""
    rect = Rect(rect.x, rect.y, game.column_count()*2+1, game.row_count()+2)
    rect = draw_frame(stdscr, rect)

    for i, (mine, flag, revealed, hint) in enumerate(zip(game.mines, game.flags,
                                               game.revealed, game.hints)):
        x, y = game.mines.linear_to_subscript(i)
        x = x*2 + rect.x # add padding between characters to get a nicer aspect ratio
        y = y + rect.y
        if revealed:
            if mine and not flag:
                stdscr.addstr(y, x, "\u26ED") # gear without hub
            elif mine and flag:
                stdscr.addstr(y, x, "\u26F3") # flag in hole
            else:
                if hint == 0:
                    stdscr.addstr(y, x, " ")
                else:
                    stdscr.addstr(y, x, str(hint), curses.A_DIM)
        else:
            if flag:
                stdscr.addstr(y, x, "\u26F3") # flag in hole
            else:
                stdscr.addstr(y, x, "?")

    return rect

def draw_header(stdscr, game):
    """Draws some info about in the first line."""
    if game.is_solved():
        text = "Congratulations, You Won!"
    elif game.is_lost():
        text = "You Lost!"
    else:
        remaining = game.number_of_mines() - game.number_of_flags()
        text = "Remaining Mines: {0}".format(remaining)
    stdscr.addstr(0, 0, text, curses.A_REVERSE)
    return Rect(0, 0, curses.COLS-1, 1)

def draw_footer(stdscr, game):
    """Displays the controls in the last line."""
    if game.is_lost() or game.is_solved():
        controls = [("Press any key to continue", "")]
    else:
        controls = [
            ("Navigate:", "\u2190 \u2192 \u2191 \u2193"),
            ("Reveal:", "Space \u2423"),
            ("Toggle Mark:", "Enter \u23CE"),
            ("Menu:", "Escape"),
        ]
    offset = 0
    for name, control in controls:
        stdscr.addstr(curses.LINES-1, offset, name, curses.A_REVERSE)
        offset += len(name)
        stdscr.addstr(curses.LINES-1, offset, " " + control + " ")
        offset += len(control) + 2
    return Rect(0, curses.LINES-1, curses.COLS-1, 1)

def draw_screen(stdscr, game):
    """Draws the complete screen including header, game and footer."""
    header_rect = draw_header(stdscr, game)
    footer_rect = draw_footer(stdscr, game)
    game_rect = Rect(0, header_rect.height, curses.COLS-1, curses.LINES-1-header_rect.height-footer_rect.height)
    game_rect = draw_game(stdscr, game_rect, game)
    return game_rect

def cursor_to_index(cursor_pos, game_rect):
    """Converts the absolute cursor_pos to a game field index."""
    return ((cursor_pos.x - game_rect.x)//2, cursor_pos.y - game_rect.y)

def open_menu(stdscr, items):
    """Opens a menu containing items and returns the selected item.
    Blocks until the user selected an item.
    """
    width = max(map(len, items)) + 20
    height = len(items*2)-1 + 4 # +2 for frame, +2 for padding
    curses.curs_set(False)
    selected = 0

    while True:
        center = (curses.COLS//2, curses.LINES//2)
        menu_rect = Rect(center[0]-width//2, center[1]-height//2, width, height)
        menu_rect = draw_frame(stdscr, menu_rect, thick_border=True)
        for i, item in enumerate(items):
            attr = curses.A_NORMAL
            if i == selected:
                attr = curses.A_STANDOUT
            stdscr.addstr(menu_rect.y + 1 + i*2, center[0] - len(item)//2, item, attr)

        c = stdscr.getch()
        if c == curses.KEY_UP:
            selected -= 1
        if c == curses.KEY_DOWN:
            selected += 1
        if c == curses.KEY_ENTER or c == 10:
            break
        selected = clamp(selected, 0, len(items)-1)
    curses.curs_set(True)
    return items[selected]

def open_difficulty_menu(stdscr):
    """Opens a menu for the user to select a difficulty level.
    Returns a tuple with the columns and rows for the game with the
    chosen difficulty and the number of mines.
    """
    difficulty = open_menu(stdscr, items=("Easy", "Medium", "Hard"))
    if difficulty == "Easy":
        columns = 10
        rows = 10
        num_mines = int(columns*rows*0.1) # 10% of all fields are mines
    elif difficulty == "Hard":
        columns = 20
        rows = 20
        num_mines = int(columns*rows*0.1)
    else:
        columns = 15
        rows = 15
        num_mines = int(columns*rows*0.1)
    return (columns, rows, num_mines)

def main(stdscr):
    while True:
        selected = open_menu(stdscr, items=("New Game", "Exit"))
        if selected == "Exit":
            return
        if selected == "New Game":
            columns, rows, num_mines = open_difficulty_menu(stdscr)

        columns = clamp(columns, 0, curses.COLS-3) # 2 for frame
        rows = clamp(rows, 0, curses.LINES-5) # 2 for frame, 2 for header+footer

        game_loop(stdscr, columns, rows, num_mines)

def game_loop(stdscr, columns, rows, num_mines):
    game = minesweeper.Game.create_random(columns, rows, num_mines)

    Point = namedtuple('Point', ['x', 'y'], verbose=True)
    cursor_pos = Point(0, 0)

    while True:
        stdscr.clear()
        game_rect = draw_screen(stdscr, game)

        # restrict cursor to the game field
        cursor_pos = Point(
            clamp(cursor_pos.x, game_rect.x, game_rect.x+game_rect.width-1),
            clamp(cursor_pos.y, game_rect.y, game_rect.y+game_rect.height-1)
        )
        stdscr.move(cursor_pos.y, cursor_pos.x)
        stdscr.refresh()

        c = stdscr.getch()
        if c == curses.KEY_LEFT:
            cursor_pos = Point(cursor_pos.x-2, cursor_pos.y)
        if c == curses.KEY_RIGHT:
            cursor_pos = Point(cursor_pos.x+2, cursor_pos.y)
        if c == curses.KEY_UP:
            cursor_pos = Point(cursor_pos.x, cursor_pos.y-1)
        if c == curses.KEY_DOWN:
            cursor_pos = Point(cursor_pos.x, cursor_pos.y+1)
        if c == curses.KEY_ENTER or c == 10:
            game.toggle_mark(*cursor_to_index(cursor_pos, game_rect))
        if c == " " or c == 32:
            game.reveal(*cursor_to_index(cursor_pos, game_rect))
        if c == 27: # Escape
            selected = open_menu(stdscr, ["Continue", "New Game", "Exit"])
            if selected == "Exit":
                return
            elif selected == "New Game":
                columns, rows, num_mines = open_difficulty_menu(stdscr)
                return game_loop(stdscr, columns, rows, num_mines)

        if game.is_lost() or game.is_solved():
            # reveal the complete solution
            game.reveal_all()
            stdscr.clear()
            draw_screen(stdscr, game)

            # wait for user to press any key
            curses.curs_set(False)
            c = stdscr.getch()
            curses.curs_set(True)
            break

if __name__ == '__main__':
    try:
        os.environ.setdefault('ESCDELAY', '25') # descrease the escape key delay
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass

import minesweeper
import pyotherside

game = None

def log(message):
    pyotherside.send("logging", message)

def game_to_js():
    """Returns the game as a linear list of tuples (mine, flag, hint)."""
    fields = zip(game.mines, game.flags, game.revealed, game.hints)
    return [{"mine": m, "flag": f, "revealed": r, "hint": h} for m, f, r, h in fields]

def setup_game(columns, rows, mines):
    global game
    log("Creating game {0}x{1}".format(columns, rows))
    game = minesweeper.Game.create_random(columns, rows, mines)
    return game_to_js()

def number_of_flags():
    if not game:
        return 0

    return game.number_of_flags()

def update():
    if game.is_lost() or game.is_solved():
        pyotherside.send("game_state_changed", game.is_solved())
        game.reveal_all()
    pyotherside.send("fields_changed", game_to_js())

def reveal(column, row):
    """Reveals a field and sends the fields_changed event."""
    if not game:
        return

    game.reveal(int(column), int(row))
    update()

def mark(column, row):
    """Toggles a mark on a field and sends the fields_changed event."""
    if not game:
        return

    game.toggle_mark(int(column), int(row))
    update()

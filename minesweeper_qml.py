import minesweeper
import pyotherside

game = None

def log(message):
    pyotherside.send("logging", message)

def game_to_js():
    """Returns the game as a linear list of tuples (mine, flag, hint)."""
    fields = zip(game.mines, game.flags, game.hints)
    return [{"mine": m, "flag": f.value, "hint": h} for m, f, h in fields]

def setup_game(columns, rows):
    global game
    log("Creating game {0}x{1}".format(columns, rows))
    game = minesweeper.Game.create_random(columns, rows, int(columns*rows*0.1))
    return game_to_js()

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

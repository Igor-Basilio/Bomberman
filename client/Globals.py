
from threading import Lock


SCREEN_WIDTH = 672
SCREEN_HEIGHT = 672

rect_position_lock = Lock()
players_lock = Lock()
background = None
numberOfPlacedBombs = 0


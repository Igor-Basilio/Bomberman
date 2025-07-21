
from threading import Lock

#672
SCREEN_WIDTH = 624
SCREEN_HEIGHT = 624

rect_position_lock = Lock()
players_lock = Lock()
background = None
numberOfPlacedBombs = 0


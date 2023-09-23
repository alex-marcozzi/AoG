import pyglet
import src.helpers.globals as globals
from src.helpers.interfaces import Pair

def block_width(window: pyglet.window.Window):
    return window.width * globals.BLOCK_SIZE_RATE

def std_speed(window: pyglet.window.Window):
    return block_width(window) * globals.SPEED_RATE

def gravity(window: pyglet.window.Window):
    return block_width(window) * globals.GRAVITY_RATE

def add_tuples(t1: tuple, t2: tuple):
    return tuple(map(lambda x, y: x + y, t1, t2))

############################################################
#                                                          #
#                                                          #
#                                                          #
#  ---------       ---------       ---------               #
#  |       |       |       |       |       |               #
#  ---------       ---------       ---------               #
#       ------      ------       ------                    #
#       |    |      |    |       |    |                    #
#       ------      ------       ------                    #
#                                                          #
#                                                          #
#                                                          #
############################################################

# t1 is the checker, t2 is the checkee
def is_down_collision(t1: Pair, t2: Pair, block_w: float):
    t1_bottom_left = t1
    t1_bottom_right = Pair(t1.first + block_w, t1.second)
    t1_top_left = Pair(t1.first, t1.second + block_w)
    t1_top_right = Pair(t1.first + block_w, t1.second + block_w)
    t2_bottom_left = t2.copy()
    t2_bottom_right = Pair(t2.first + block_w, t2.second)
    t2_top_left = Pair(t2.first, t2.second + block_w)
    t2_top_right = Pair(t2.first + block_w, t2.second + block_w)
    if (
        ((t1_bottom_left.first < t2_top_right.first) and (t1_bottom_left.second < t2_top_right.second)) or
        ((t1_bottom_right.first < t2_top_left.first) and (t1_bottom_right.second < t2_top_left.second))
    ):
        return True
    
    return False
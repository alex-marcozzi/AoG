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
#  ---------       ---------       ---------       ------  #
#  |       |       |       |       |       |       |    |  #
#  ---------       ---------       ---------       ------  #
#       ------      ------       ------        ---------   #
#       |    |      |    |       |    |        |       |   #
#       ------      ------       ------        ---------   #
#                                                          #
############################################################

# VERIFIED WORKING
# t1 is the checker, t2 is the checkee
def is_down_collision(t1: Pair, t2: Pair, block_w: float):
    t1_bottom_left = t1.copy()
    t1_bottom_right = Pair(t1.first + block_w, t1.second)
    t1_top_left = Pair(t1.first, t1.second + block_w)
    t1_top_right = Pair(t1.first + block_w, t1.second + block_w)
    t2_bottom_left = t2.copy()
    t2_bottom_right = Pair(t2.first + block_w, t2.second)
    t2_top_left = Pair(t2.first, t2.second + block_w)
    t2_top_right = Pair(t2.first + block_w, t2.second + block_w)
    
    # # first check if t1 is above t2
    if t2_top_left.first < t1_top_right.first and t2_top_right.first > t1_bottom_left.first:
        # then check if they are colliding
        if t1_bottom_left.second <= t2_top_left.second:
            return True
    
    return False

# VERIFIED WORKING
# t1 is the checker, t2 is the checkee
def is_right_collision(t1: Pair, t2: Pair, block_w: float):
    t1_bottom_left = t1.copy()
    t1_bottom_right = Pair(t1.first + block_w, t1.second)
    t1_top_left = Pair(t1.first, t1.second + block_w)
    t1_top_right = Pair(t1.first + block_w, t1.second + block_w)
    t2_bottom_left = t2.copy()
    t2_bottom_right = Pair(t2.first + block_w, t2.second)
    t2_top_left = Pair(t2.first, t2.second + block_w)
    t2_top_right = Pair(t2.first + block_w, t2.second + block_w)

    # first check if t1 is level with t2
    if t1_bottom_right.second < t2_top_left.second and t1_top_right.second > t2_bottom_left.second:
        # then check if they are colliding
        if t1_top_right.first >= t2_top_left.first:
            return True
    
    return False

# VERIFIED WORKING
# t1 is the checker, t2 is the checkee
def is_left_collision(t1: Pair, t2: Pair, block_w: float):
    t1_bottom_left = t1.copy()
    t1_bottom_right = Pair(t1.first + block_w, t1.second)
    t1_top_left = Pair(t1.first, t1.second + block_w)
    t1_top_right = Pair(t1.first + block_w, t1.second + block_w)
    t2_bottom_left = t2.copy()
    t2_bottom_right = Pair(t2.first + block_w, t2.second)
    t2_top_left = Pair(t2.first, t2.second + block_w)
    t2_top_right = Pair(t2.first + block_w, t2.second + block_w)

    # first check if t1 is level with t2
    if t1_bottom_left.second < t2_top_right.second and t1_top_left.second > t2_bottom_right.second:
        # then check if they are colliding
        if t1_top_left.first <= t2_top_right.first:
            return True
    
    return False

# t1 is the checker, t2 is the checkee
def is_up_collision(t1: Pair, t2: Pair, block_w: float):
    t1_bottom_left = t1.copy()
    t1_bottom_right = Pair(t1.first + block_w, t1.second)
    t1_top_left = Pair(t1.first, t1.second + block_w)
    t1_top_right = Pair(t1.first + block_w, t1.second + block_w)
    t2_bottom_left = t2.copy()
    t2_bottom_right = Pair(t2.first + block_w, t2.second)
    t2_top_left = Pair(t2.first, t2.second + block_w)
    t2_top_right = Pair(t2.first + block_w, t2.second + block_w)

    # first check if t1 is level with t2
    if t1_top_left.first < t2_bottom_right.first and t1_top_right.first > t2_bottom_left.first:
        # then check if they are colliding
        if t1_top_left.second >= t2_bottom_left.second:
            return True
    
    return False
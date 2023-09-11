import pyglet
import src.helpers.globals as globals

def block_width(window: pyglet.window.Window):
    return window.width * globals.BLOCK_SIZE_RATE

def std_speed(window: pyglet.window.Window):
    return block_width(window) * globals.SPEED_RATE

def gravity(window: pyglet.window.Window):
    return block_width(window) * globals.GRAVITY_RATE

def add_tuples(t1: tuple, t2: tuple):
    return tuple(map(lambda x, y: x + y, t1, t2))

# t1 is the checker, t2 is the checkee
def is_down_collision(t1: tuple, t2: tuple, block_w: float):
    t1_bottom_left = t1
    t1_bottom_right = (t1[0] + block_w, t1[1])
    t1_top_left = (t1[0], t1[1] + block_w)
    t1_top_right = (t1[0] + block_w, t1[1] + block_w)
    t2_bottom_left = t2
    t2_bottom_right = (t2[0] + block_w, t2[1])
    t2_top_left = (t2[0], t2[1] + block_w)
    t2_top_right = (t2[0] + block_w, t2[1] + block_w)
    if (
        ((t1_bottom_left[0] < t2_top_right[0]) and (t1_bottom_left[1] < t2_top_right[1])) or
        ((t1_bottom_right[0] < t2_top_left[0]) and (t1_bottom_right[1] < t2_top_left[1]))
    ):
        return True
    
    return False
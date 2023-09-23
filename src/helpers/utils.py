import pyglet
import src.helpers.globals as globals
from src.helpers.interfaces import Pair
from src.entity import Entity

def block_width(window: pyglet.window.Window):
    return window.width * globals.BLOCK_SIZE_RATE

def std_speed(window: pyglet.window.Window):
    return block_width(window) * globals.SPEED_RATE

def gravity(window: pyglet.window.Window):
    return block_width(window) * globals.GRAVITY_RATE

def add_tuples(entity1: tuple, entity2: tuple):
    return tuple(map(lambda x, y: x + y, entity1, entity2))

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
# entity1 is the checker, entity2 is the checkee
def is_down_collision(entity1: Entity, entity2: Entity):
    e1_next_pos = entity1.nextPos()
    e2_next_pos = entity2.nextPos()

    entity1_bottom_left = e1_next_pos.copy()
    entity1_bottom_right = Pair(e1_next_pos.first + entity1.sprite.width, e1_next_pos.second)
    entity1_top_left = Pair(e1_next_pos.first, e1_next_pos.second + entity1.sprite.height)
    entity1_top_right = Pair(e1_next_pos.first + entity1.sprite.width, e1_next_pos.second + entity1.sprite.height)
    entity2_bottom_left = e2_next_pos.copy()
    entity2_bottom_right = Pair(e2_next_pos.first + entity2.sprite.width, e2_next_pos.second)
    entity2_top_left = Pair(e2_next_pos.first, e2_next_pos.second + entity2.sprite.height)
    entity2_top_right = Pair(e2_next_pos.first + entity2.sprite.width, e2_next_pos.second + entity2.sprite.height)
    
    # # first check if entity1 is above entity2
    if entity2_top_left.first <= entity1_top_right.first and entity2_top_right.first >= entity1_bottom_left.first:
        # then check if they are colliding
        if entity1_bottom_left.second <= entity2_top_left.second and entity1_bottom_left.second >= entity2_bottom_left.second:
            return True
    
    return False

# VERIFIED WORKING
# entity1 is the checker, entity2 is the checkee
def is_right_collision(entity1: Entity, entity2: Entity):
    e1_next_pos = entity1.nextPos()
    e2_next_pos = entity2.nextPos()

    entity1_bottom_left = e1_next_pos
    entity1_bottom_right = Pair(e1_next_pos.first + entity1.sprite.width, e1_next_pos.second)
    entity1_top_left = Pair(e1_next_pos.first, e1_next_pos.second + entity1.sprite.height)
    entity1_top_right = Pair(e1_next_pos.first + entity1.sprite.width, e1_next_pos.second + entity1.sprite.height)
    entity2_bottom_left = e2_next_pos
    entity2_bottom_right = Pair(e2_next_pos.first + entity2.sprite.width, e2_next_pos.second)
    entity2_top_left = Pair(e2_next_pos.first, e2_next_pos.second + entity2.sprite.height)
    entity2_top_right = Pair(e2_next_pos.first + entity2.sprite.width, e2_next_pos.second + entity2.sprite.height)

    # first check if entity1 is level with entity2
    if entity1_bottom_right.second < entity2_top_left.second and entity1_top_right.second > entity2_bottom_left.second:
        # then check if they are colliding
        if entity1_top_right.first >= entity2_top_left.first:
            return True
    
    return False

# VERIFIED WORKING
# entity1 is the checker, entity2 is the checkee
def is_left_collision(entity1: Entity, entity2: Entity):
    e1_next_pos = entity1.nextPos()
    e2_next_pos = entity2.nextPos()

    entity1_bottom_left = e1_next_pos
    entity1_bottom_right = Pair(e1_next_pos.first + entity1.sprite.width, e1_next_pos.second)
    entity1_top_left = Pair(e1_next_pos.first, e1_next_pos.second + entity1.sprite.height)
    entity1_top_right = Pair(e1_next_pos.first + entity1.sprite.width, e1_next_pos.second + entity1.sprite.height)
    entity2_bottom_left = e2_next_pos
    entity2_bottom_right = Pair(e2_next_pos.first + entity2.sprite.width, e2_next_pos.second)
    entity2_top_left = Pair(e2_next_pos.first, e2_next_pos.second + entity2.sprite.height)
    entity2_top_right = Pair(e2_next_pos.first + entity2.sprite.width, e2_next_pos.second + entity2.sprite.height)

    # first check if entity1 is level with entity2
    if entity1_bottom_left.second < entity2_top_right.second and entity1_top_left.second > entity2_bottom_right.second:
        # then check if they are colliding
        if entity1_top_left.first <= entity2_top_right.first:
            return True
    
    return False

# entity1 is the checker, entity2 is the checkee
def is_up_collision(entity1: Entity, entity2: Entity):
    e1_next_pos = entity1.nextPos()
    e2_next_pos = entity2.nextPos()

    print(e1_next_pos.first)
    print(e1_next_pos.second)
    print(e2_next_pos.first)
    print(e2_next_pos.second)
    
    entity1_bottom_left = e1_next_pos
    entity1_bottom_right = Pair(e1_next_pos.first + entity1.sprite.width, e1_next_pos.second)
    entity1_top_left = Pair(e1_next_pos.first, e1_next_pos.second + entity1.sprite.height)
    entity1_top_right = Pair(e1_next_pos.first + entity1.sprite.width, e1_next_pos.second + entity1.sprite.height)
    entity2_bottom_left = e2_next_pos
    entity2_bottom_right = Pair(e2_next_pos.first + entity2.sprite.width, e2_next_pos.second)
    entity2_top_left = Pair(e2_next_pos.first, e2_next_pos.second + entity2.sprite.height)
    entity2_top_right = Pair(e2_next_pos.first + entity2.sprite.width, e2_next_pos.second + entity2.sprite.height)

    # first check if entity1 is level with entity2
    if entity1_top_left.first < entity2_bottom_right.first and entity1_top_right.first > entity2_bottom_left.first:
        # then check if they are colliding
        if entity1_top_left.second >= entity2_bottom_left.second:
            return True
    
    return False
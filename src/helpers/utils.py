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

def normalize_vector(v: Pair):
    # distance = (v.first * v.first) + (v.second * v.second)  # hypotenuse squared

    # if distance == 0:
    #     return v.copy()
    
    return Pair(v.first / 10, v.second / 10)

def float_eq(f1: float, f2: float, margin: float = 1):
    return (abs(f1 - f2) <= margin)

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

# pointer moves along the vector line in normalized steps
# from start to end
def is_right_collision_new(entity1: Entity, entity2: Entity):
    if entity1.velocity.first <= 0:
        return False
    
    e1_next = entity1.copy()
    e2_next = entity2.copy()

    e1_next.tick_pos_only()  # move to next position
    e2_next.tick_pos_only()
    
    e1_pointer = entity1.copy()
    e2_pointer = entity2.copy()
    
    e1_pointer.velocity = normalize_vector(entity1.velocity)
    e2_pointer.velocity = normalize_vector(entity2.velocity)

    # loop and move pointer until we reach the end
    while not float_eq(e1_pointer.bottomRight().first, e1_next.bottomRight().first):
        if e1_pointer.bottomRight().second < e2_pointer.topLeft().second and e1_pointer.topRight().second > e2_pointer.bottomLeft().second:
            if float_eq(e1_pointer.bottomRight().first, e2_pointer.bottomLeft().first):
                return True
        e1_pointer.tick_pos_only()
    
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

# pointer moves along the vector line in normalized steps
# from start to end
def is_left_collision_new(entity1: Entity, entity2: Entity):
    if entity1.velocity.first >= 0:
        return False
    
    e1_next = entity1.copy()
    e2_next = entity2.copy()

    e1_next.tick_pos_only()  # move to next position
    e2_next.tick_pos_only()
    
    e1_pointer = entity1.copy()
    e2_pointer = entity2.copy()
    
    e1_pointer.velocity = normalize_vector(entity1.velocity)
    e2_pointer.velocity = normalize_vector(entity2.velocity)

    # loop and move pointer until we reach the end
    while not float_eq(e1_pointer.bottomRight().first, e1_next.bottomRight().first):
        # if entity1_bottom_left.second < entity2_top_right.second and entity1_top_left.second > entity2_bottom_right.second:
        if e1_pointer.bottomLeft().second < e2_pointer.topRight().second and e1_pointer.topLeft().second > e2_pointer.bottomRight().second:
            print("HEREEEEE")
            if float_eq(e1_pointer.bottomLeft().first, e2_pointer.bottomRight().first):
                return True
        e1_pointer.tick_pos_only()
    
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
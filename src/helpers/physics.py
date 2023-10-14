import pyglet
from src.helpers.interfaces import Pair
from src.entity import Entity
from src.hitbox import Hitbox


def normalize_vector(v: Pair):

    return Pair(
        v.first / 100, v.second / 100
    )  # smaller slices means more precision, but more computationally expensive


def float_eq(f1: float, f2: float, margin: float = 1):
    return abs(f1 - f2) <= margin


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

# pointer moves along the vector line in normalized steps
# from start to end
def is_down_collision(dt: float, entity1: Entity, entity2: Entity):
    e1_next = entity1.copy()
    e2_next = entity2.copy()

    e1_next.tick_pos_only(dt)  # move to next position
    e2_next.tick_pos_only(dt)

    crossed_y = entity1.bottomLeft().second >= entity2.topLeft().second and e1_next.bottomLeft().second <= e2_next.topLeft().second
    x_is_in_line = e1_next.bottomLeft().first < e2_next.topRight().first and e1_next.bottomRight().first > e2_next.topLeft().first

    if crossed_y and x_is_in_line:
        return True
        
    return False


# pointer moves along the vector line in normalized steps
# from start to end
def is_right_collision(dt: float, entity1: Entity, entity2: Entity):
    e1_next = entity1.copy()
    e2_next = entity2.copy()

    e1_next.tick_pos_only(dt)  # move to next position
    e2_next.tick_pos_only(dt)

    crossed_x = entity1.bottomRight().first <= entity2.bottomLeft().first and e1_next.bottomRight().first >= e2_next.bottomLeft().first
    y_is_in_line = e1_next.bottomRight().second < e2_next.topLeft().second and e1_next.topRight().second > e2_next.bottomLeft().second

    if crossed_x and y_is_in_line:
        return True
        
    return False


def is_left_collision(dt: float, entity1: Entity, entity2: Entity):
    e1_next = entity1.copy()
    e2_next = entity2.copy()

    e1_next.tick_pos_only(dt)  # move to next position
    e2_next.tick_pos_only(dt)

    crossed_x = entity1.bottomLeft().first >= entity2.bottomRight().first and e1_next.bottomLeft().first <= e2_next.bottomRight().first
    y_is_in_line = e1_next.bottomLeft().second < e2_next.topRight().second and e1_next.topLeft().second > e2_next.bottomRight().second

    if crossed_x and y_is_in_line:
        return True
        
    return False


# pointer moves along the vector line in normalized steps
# from start to end
def is_up_collision(dt: float, entity1: Entity, entity2: Entity):
    e1_next = entity1.copy()
    e2_next = entity2.copy()

    e1_next.tick_pos_only(dt)  # move to next position
    e2_next.tick_pos_only(dt)

    crossed_y = entity1.topLeft().second <= entity2.bottomLeft().second and e1_next.topLeft().second >= e2_next.bottomLeft().second
    x_is_in_line = e1_next.topLeft().first < e2_next.bottomRight().first and e1_next.topRight().first > e2_next.bottomLeft().first

    if crossed_y and x_is_in_line:
        return True
        
    return False


def is_overlap(dt: float, entity1: Entity, entity2: Entity):
    return is_overlap(entity1.hitbox, entity2.hitbox)

def is_overlap(dt: float, hitbox1: Hitbox, hitbox2: Hitbox):
    if hitbox1.topLeft().second >= hitbox2.bottomRight().second and hitbox1.bottomLeft().second <= hitbox2.topRight().second:
        if (
            hitbox1.topLeft().first <= hitbox2.bottomRight().first
            and hitbox1.topRight().first >= hitbox2.bottomLeft().first
        ):
            return True

    return False

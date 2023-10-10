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
def is_down_collision(entity1: Entity, entity2: Entity):
    if entity1.velocity.second > 0:
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

    first = True
    while first or not float_eq(
        e1_pointer.bottomRight().second, e1_next.bottomRight().second
    ):
        first = False
        if (
            e1_pointer.bottomLeft().first < e2_pointer.topRight().first
            and e1_pointer.bottomRight().first > e2_pointer.topLeft().first
        ):
            if float_eq(e1_pointer.bottomLeft().second, e2_pointer.topRight().second):
                return True

        e1_pointer.tick_pos_only()
        e2_pointer.tick_pos_only()

    return False


# pointer moves along the vector line in normalized steps
# from start to end
def is_right_collision(entity1: Entity, entity2: Entity):
    if entity1.velocity.first < 0:
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
    first = True
    while first or not float_eq(
        e1_pointer.bottomRight().first, e1_next.bottomRight().first
    ):
        first = False
        if (
            e1_pointer.bottomRight().second < e2_pointer.topLeft().second
            and e1_pointer.topRight().second > e2_pointer.bottomLeft().second
        ):
            if float_eq(e1_pointer.bottomRight().first, e2_pointer.bottomLeft().first):
                return True
        e1_pointer.tick_pos_only()
        e2_pointer.tick_pos_only()

    return False


def is_left_collision(entity1: Entity, entity2: Entity):
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
    first = True
    while first or not float_eq(
        e1_pointer.bottomRight().first, e1_next.bottomRight().first
    ):
        first = False
        if (
            e1_pointer.bottomLeft().second < e2_pointer.topRight().second
            and e1_pointer.topLeft().second > e2_pointer.bottomRight().second
        ):
            if float_eq(e1_pointer.bottomLeft().first, e2_pointer.bottomRight().first):
                return True
        e1_pointer.tick_pos_only()
        e2_pointer.tick_pos_only()

    return False


# pointer moves along the vector line in normalized steps
# from start to end
def is_up_collision(entity1: Entity, entity2: Entity):
    if entity1.velocity.second <= 0:
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
    first = True
    while first or not float_eq(
        e1_pointer.bottomRight().second, e1_next.bottomRight().second
    ):
        first = False
        if (
            e1_pointer.topLeft().first < e2_pointer.bottomRight().first
            and e1_pointer.topRight().first > e2_pointer.bottomLeft().first
        ):
            if float_eq(e1_pointer.topLeft().second, e2_pointer.bottomLeft().second):
                return True

        e1_pointer.tick_pos_only()
        e2_pointer.tick_pos_only()

    return False


def is_overlap(entity1: Entity, entity2: Entity):
    return is_overlap(entity1.hitbox, entity2.hitbox)
    # if entity1.topLeft().second >= entity2.bottomRight().second:
    #     if (
    #         entity1.topLeft().first <= entity2.bottomRight().first
    #         and entity1.topRight().first >= entity2.bottomLeft().first
    #     ):
    #         return True

    # if entity2.topLeft().second >= entity1.bottomRight().second:
    #     if (
    #         entity2.topLeft().first <= entity1.bottomRight().first
    #         and entity2.topRight().first >= entity1.bottomLeft().first
    #     ):
    #         return True

    # return False

def is_overlap(hitbox1: Hitbox, hitbox2: Hitbox):
    if hitbox1.topLeft().second >= hitbox2.bottomRight().second and hitbox1.bottomLeft().second <= hitbox2.topRight().second:
        if (
            hitbox1.topLeft().first <= hitbox2.bottomRight().first
            and hitbox1.topRight().first >= hitbox2.bottomLeft().first
        ):
            return True

    return False

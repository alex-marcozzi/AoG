import pyglet
from src.helpers.interfaces import Pair
from src.entity import Entity
from src.hitbox import Hitbox
from src.entity_classes.character_classes.player import Player
from src.entity_classes.block_classes.moving_block_new import MovingBlockNew


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
    debug = False
    if entity2.id == "101":
        debug = True
    return is_hitbox_down_collision(dt, entity1.hitbox, entity2.hitbox, entity1.velocity, entity2.velocity, debug)


    e1_next = entity1.copy()
    e2_next = entity2.copy()

    if isinstance(type(entity2), MovingBlockNew):
        print(f"player: {entity1.global_pos.first}, {entity1.global_pos.second} ---> {e1_next.global_pos.first}, {e1_next.global_pos.second}")
        print(f"mblock: {entity2.global_pos.first}, {entity2.global_pos.second} ---> {e2_next.global_pos.first}, {e2_next.global_pos.second}")

    # e1_next.tick_pos_only(dt)  # move to next position
    # e2_next.tick_pos_only(dt)
    e1_next.global_pos.add(Pair(entity1.velocity.first * dt, entity1.velocity.second * dt))
    e2_next.global_pos.add(Pair(entity2.velocity.first * dt, entity2.velocity.second * dt))

    crossed_y = entity1.bottomLeft().second >= entity2.topLeft().second and e1_next.bottomLeft().second <= e2_next.topLeft().second
    x_is_in_line = e1_next.bottomLeft().first < e2_next.topRight().first and e1_next.bottomRight().first > e2_next.topLeft().first

    if crossed_y and x_is_in_line:
        return True
        
    return False

def is_hitbox_down_collision(dt: float, hitbox1: Hitbox, hitbox2: Hitbox, velocity1: Pair, velocity2: Pair, debug = False):
    h1_next = hitbox1.copy()
    h1_next.pos.add(Pair(velocity1.first * dt, velocity1.second * dt))
    h2_next = hitbox2.copy()
    h2_next.pos.add(Pair(velocity2.first * dt, velocity2.second * dt))

    if debug:
        print(f"crossed_y: {hitbox1.bottomLeft().second} >= {hitbox2.topLeft().second} and {h1_next.bottomLeft().second} <= {h2_next.topLeft().second}")
        print(f"x_in_line: {h1_next.bottomLeft().first} < {h2_next.topRight().first} and {h1_next.bottomRight().first} > {h2_next.topLeft().first}")


    crossed_y = hitbox1.bottomLeft().second >= hitbox2.topLeft().second - 1 and h1_next.bottomLeft().second <= h2_next.topLeft().second
    x_is_in_line = h1_next.bottomLeft().first < h2_next.topRight().first and h1_next.bottomRight().first > h2_next.topLeft().first

    if crossed_y and x_is_in_line:
        return True
        
    return False


# pointer moves along the vector line in normalized steps
# from start to end
def is_right_collision(dt: float, entity1: Entity, entity2: Entity):
    return is_hitbox_right_collision(dt, entity1.hitbox, entity2.hitbox, entity1.velocity, entity2.velocity)

    e1_next = entity1.copy()
    e2_next = entity2.copy()

    e1_next.global_pos.add(Pair(entity1.velocity.first * dt, entity1.velocity.second * dt))
    e2_next.global_pos.add(Pair(entity2.velocity.first * dt, entity2.velocity.second * dt))

    crossed_x = entity1.bottomRight().first <= entity2.bottomLeft().first and e1_next.bottomRight().first >= e2_next.bottomLeft().first
    y_is_in_line = e1_next.bottomRight().second < e2_next.topLeft().second and e1_next.topRight().second > e2_next.bottomLeft().second


    if crossed_x and y_is_in_line:
        return True
        
    return False


# pointer moves along the vector line in normalized steps
# from start to end
def is_hitbox_right_collision(dt: float, hitbox1: Hitbox, hitbox2: Hitbox, velocity1: Pair, velocity2: Pair):
    h1_next = hitbox1.copy()
    h1_next.pos.add(Pair(velocity1.first * dt, velocity1.second * dt))
    h2_next = hitbox2.copy()
    h2_next.pos.add(Pair(velocity2.first * dt, velocity2.second * dt))

    crossed_x = hitbox1.bottomRight().first <= hitbox2.bottomLeft().first and h1_next.bottomRight().first >= h2_next.bottomLeft().first
    y_is_in_line = h1_next.bottomRight().second < h2_next.topLeft().second and h1_next.topRight().second > h2_next.bottomLeft().second


    if crossed_x and y_is_in_line:
        return True
        
    return False


def is_left_collision(dt: float, entity1: Entity, entity2: Entity):
    return is_hitbox_left_collision(dt, entity1.hitbox, entity2.hitbox, entity1.velocity, entity2.velocity)
    e1_next = entity1.copy()
    e2_next = entity2.copy()

    # e1_next.tick_pos_only(dt)  # move to next position
    # e2_next.tick_pos_only(dt)
    e1_next.global_pos.add(Pair(entity1.velocity.first * dt, entity1.velocity.second * dt))
    e2_next.global_pos.add(Pair(entity2.velocity.first * dt, entity2.velocity.second * dt))

    crossed_x = entity1.bottomLeft().first >= entity2.bottomRight().first and e1_next.bottomLeft().first <= e2_next.bottomRight().first
    y_is_in_line = e1_next.bottomLeft().second < e2_next.topRight().second and e1_next.topLeft().second > e2_next.bottomRight().second

    if crossed_x and y_is_in_line:
        return True
        
    return False


# pointer moves along the vector line in normalized steps
# from start to end
def is_hitbox_left_collision(dt: float, hitbox1: Hitbox, hitbox2: Hitbox, velocity1: Pair, velocity2: Pair):
    h1_next = hitbox1.copy()
    h1_next.pos.add(Pair(velocity1.first * dt, velocity1.second * dt))
    h2_next = hitbox2.copy()
    h2_next.pos.add(Pair(velocity2.first * dt, velocity2.second * dt))

    crossed_x = hitbox1.bottomLeft().first >= hitbox2.bottomRight().first and h1_next.bottomLeft().first <= h2_next.bottomRight().first
    y_is_in_line = h1_next.bottomLeft().second < h2_next.topRight().second and h1_next.topLeft().second > h2_next.bottomRight().second

    if crossed_x and y_is_in_line:
        return True
        
    return False


# pointer moves along the vector line in normalized steps
# from start to end
def is_up_collision(dt: float, entity1: Entity, entity2: Entity):
    return is_hitbox_up_collision(dt, entity1.hitbox, entity2.hitbox, entity1.velocity, entity2.velocity)
    e1_next = entity1.copy()
    e2_next = entity2.copy()

    # e1_next.tick_pos_only(dt)  # move to next position
    # e2_next.tick_pos_only(dt)
    e1_next.global_pos.add(Pair(entity1.velocity.first * dt, entity1.velocity.second * dt))
    e2_next.global_pos.add(Pair(entity2.velocity.first * dt, entity2.velocity.second * dt))

    crossed_y = entity1.topLeft().second <= entity2.bottomLeft().second and e1_next.topLeft().second >= e2_next.bottomLeft().second
    x_is_in_line = e1_next.topLeft().first <= e2_next.bottomRight().first and e1_next.topRight().first >= e2_next.bottomLeft().first

    if crossed_y and x_is_in_line:
        return True
        
    return False


# pointer moves along the vector line in normalized steps
# from start to end
def is_hitbox_up_collision(dt: float, hitbox1: Hitbox, hitbox2: Hitbox, velocity1: Pair, velocity2: Pair):
    h1_next = hitbox1.copy()
    h1_next.pos.add(Pair(velocity1.first * dt, velocity1.second * dt))
    h2_next = hitbox2.copy()
    h2_next.pos.add(Pair(velocity2.first * dt, velocity2.second * dt))

    crossed_y = hitbox1.topLeft().second <= hitbox2.bottomLeft().second and h1_next.topLeft().second >= h2_next.bottomLeft().second
    x_is_in_line = h1_next.topLeft().first <= h2_next.bottomRight().first and h1_next.topRight().first >= h2_next.bottomLeft().first

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

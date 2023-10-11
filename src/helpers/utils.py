import pyglet
import src.helpers.globals as globals

loaded_images = {}  # key: filename, value: image

def block_width(window: pyglet.window.Window):
    return window.width * globals.BLOCK_SIZE_RATE


def std_speed(window: pyglet.window.Window):
    return block_width(window) * globals.SPEED_RATE


def gravity(window: pyglet.window.Window):
    return block_width(window) * globals.GRAVITY_RATE


def add_tuples(entity1: tuple, entity2: tuple):
    return tuple(map(lambda x, y: x + y, entity1, entity2))

def make_sprite(sprite_filename: str, width: float, height: float, visible: float, batch):
        if not sprite_filename in loaded_images.keys():
            loaded_images[sprite_filename] = pyglet.resource.image(sprite_filename)
        sprite = pyglet.sprite.Sprite(
            img=loaded_images[sprite_filename], batch=batch
        )
        sprite.width = width
        sprite.height = height
        sprite.visible = visible

        return sprite

def copy_sprite(other_sprite: pyglet.sprite.Sprite):
    new_copy = pyglet.sprite.Sprite(
         img=other_sprite.image,
         x=other_sprite.x,
         y=other_sprite.y,
    )
    new_copy.width=other_sprite.width
    new_copy.height=other_sprite.height
    
    return new_copy


# def normalize_vector(v: Pair):
#     # distance = (v.first * v.first) + (v.second * v.second)  # hypotenuse squared

#     # if distance == 0:
#     #     return v.copy()

#     return Pair(v.first / 10, v.second / 10)

# def float_eq(f1: float, f2: float, margin: float = 1):
#     return (abs(f1 - f2) <= margin)

# ############################################################
# #                                                          #
# #  ---------       ---------       ---------       ------  #
# #  |       |       |       |       |       |       |    |  #
# #  ---------       ---------       ---------       ------  #
# #       ------      ------       ------        ---------   #
# #       |    |      |    |       |    |        |       |   #
# #       ------      ------       ------        ---------   #
# #                                                          #
# ############################################################

# # pointer moves along the vector line in normalized steps
# # from start to end
# def is_down_collision(entity1: Entity, entity2: Entity):
#     if entity1.velocity.second > 0:
#         return False

#     e1_next = entity1.copy()
#     e2_next = entity2.copy()

#     e1_next.tick_pos_only()  # move to next position
#     e2_next.tick_pos_only()

#     e1_pointer = entity1.copy()
#     e2_pointer = entity2.copy()

#     e1_pointer.velocity = normalize_vector(entity1.velocity)
#     e2_pointer.velocity = normalize_vector(entity2.velocity)

#     # loop and move pointer until we reach the end

#     while not float_eq(e1_pointer.bottomRight().second, e1_next.bottomRight().second):
#         if e1_pointer.bottomLeft().first < e2_pointer.topRight().first and e1_pointer.bottomRight().first > e2_pointer.topLeft().first:
#             if float_eq(e1_pointer.bottomLeft().second, e2_pointer.topRight().second):
#                 return True

#         e1_pointer.tick_pos_only()

#     return False

# # pointer moves along the vector line in normalized steps
# # from start to end
# def is_right_collision(entity1: Entity, entity2: Entity):
#     if entity1.velocity.first <= 0:
#         return False

#     e1_next = entity1.copy()
#     e2_next = entity2.copy()

#     e1_next.tick_pos_only()  # move to next position
#     e2_next.tick_pos_only()

#     e1_pointer = entity1.copy()
#     e2_pointer = entity2.copy()

#     e1_pointer.velocity = normalize_vector(entity1.velocity)
#     e2_pointer.velocity = normalize_vector(entity2.velocity)

#     # loop and move pointer until we reach the end
#     while not float_eq(e1_pointer.bottomRight().first, e1_next.bottomRight().first):
#         if e1_pointer.bottomRight().second < e2_pointer.topLeft().second and e1_pointer.topRight().second > e2_pointer.bottomLeft().second:
#             if float_eq(e1_pointer.bottomRight().first, e2_pointer.bottomLeft().first):
#                 return True
#         e1_pointer.tick_pos_only()

#     return False

# def is_left_collision(entity1: Entity, entity2: Entity):
#     if entity1.velocity.first >= 0:
#         return False

#     e1_next = entity1.copy()
#     e2_next = entity2.copy()

#     e1_next.tick_pos_only()  # move to next position
#     e2_next.tick_pos_only()

#     e1_pointer = entity1.copy()
#     e2_pointer = entity2.copy()

#     e1_pointer.velocity = normalize_vector(entity1.velocity)
#     e2_pointer.velocity = normalize_vector(entity2.velocity)

#     # loop and move pointer until we reach the end
#     while not float_eq(e1_pointer.bottomRight().first, e1_next.bottomRight().first):
#         if e1_pointer.bottomLeft().second < e2_pointer.topRight().second and e1_pointer.topLeft().second > e2_pointer.bottomRight().second:
#             if float_eq(e1_pointer.bottomLeft().first, e2_pointer.bottomRight().first):
#                 return True
#         e1_pointer.tick_pos_only()

#     return False

# # pointer moves along the vector line in normalized steps
# # from start to end
# def is_up_collision(entity1: Entity, entity2: Entity):
#     if entity1.velocity.second <= 0:
#         return False

#     e1_next = entity1.copy()
#     e2_next = entity2.copy()

#     e1_next.tick_pos_only()  # move to next position
#     e2_next.tick_pos_only()

#     e1_pointer = entity1.copy()
#     e2_pointer = entity2.copy()

#     e1_pointer.velocity = normalize_vector(entity1.velocity)
#     e2_pointer.velocity = normalize_vector(entity2.velocity)

#     # loop and move pointer until we reach the end
#     while not float_eq(e1_pointer.bottomRight().second, e1_next.bottomRight().second):
#         if e1_pointer.topLeft().first < e2_pointer.bottomRight().first and e1_pointer.topRight().first > e2_pointer.bottomLeft().first:
#             if float_eq(e1_pointer.topLeft().second, e2_pointer.bottomLeft().second):
#                 return True

#         e1_pointer.tick_pos_only()

#     return False

import pyglet
from src.entity import Entity
from src.helpers.interfaces import Pair


def initialize_level_base(x_width, y_height):
    return [[None for col in range(x_width)] for row in range(y_height)]

# sets the squares in "level_array" specified in a line from "from_pos" to "to_pos" to the "entity" object
# note: inclusive beginning, inclusive end
def set_line(level_array: list, from_pos: Pair, to_pos: Pair, entity: Entity, block_w, block_h):
    for x in range(from_pos[0], to_pos[0] + 1):
        for y in range(from_pos[1], to_pos[1] + 1):
            this_entity = entity.copy()
            this_entity.global_pos = (x * block_w, y * block_h)
            level_array[x][y] = this_entity


def build_level1(window):
    block = Entity(window, "assets/images/orange.png", global_pos=(0, 0), velocity=(0,0), acceleration=(0,0), width=window.width / 15, height = window.width / 15)
    level1 = initialize_level_base(100, 100)
    set_line(level1, (0,0), (10, 0), block, window.width / 15, window.width / 15)
    set_line(level1, (15,0), (17, 0), block, window.width / 15, window.width / 15)
    set_line(level1, (19,0), (23, 0), block, window.width / 15, window.width / 15)
    set_line(level1, (25,1), (27, 1), block, window.width / 15, window.width / 15)
    set_line(level1, (10,0), (10, 2), block, window.width / 15, window.width / 15)
    set_line(level1, (10,0), (10, 3), block, window.width / 15, window.width / 15)
    set_line(level1, (10,0), (10, 4), block, window.width / 15, window.width / 15)
    set_line(level1, (10,0), (10, 5), block, window.width / 15, window.width / 15)

    return level1
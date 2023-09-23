import pyglet
from src.entity import Entity
from src.helpers.interfaces import Pair


def initialize_level_base(x_width, y_height):
    return [[None for col in range(x_width)] for row in range(y_height)]

# sets the squares in "level_array" specified in a line from "from_pos" to "to_pos" to the "entity" object
# note: inclusive beginning, inclusive end
def set_line(level_array: list, from_pos: Pair, to_pos: Pair, entity: Entity, block_w, block_h):
    for x in range(from_pos.first, to_pos.first + 1):
        for y in range(from_pos.second, to_pos.second + 1):
            this_entity = entity.copy()
            this_entity.global_pos = Pair(x * block_w, y * block_h)
            level_array[x][y] = this_entity


def build_level1(window):
    block = Entity(window, "assets/images/orange.png", global_pos=Pair(0, 0), velocity=Pair(0,0), acceleration=Pair(0,0), width=window.width / 15, height = window.width / 15)
    level1 = initialize_level_base(100, 100)
    set_line(level1, Pair(0,0), Pair(10, 0), block, window.width / 15, window.width / 15)
    set_line(level1, Pair(15,0), Pair(17, 0), block, window.width / 15, window.width / 15)
    set_line(level1, Pair(19,0), Pair(23, 0), block, window.width / 15, window.width / 15)
    set_line(level1, Pair(25,1), Pair(27, 1), block, window.width / 15, window.width / 15)
    set_line(level1, Pair(10,0), Pair(10, 2), block, window.width / 15, window.width / 15)
    set_line(level1, Pair(10,0), Pair(10, 3), block, window.width / 15, window.width / 15)
    set_line(level1, Pair(10,0), Pair(10, 4), block, window.width / 15, window.width / 15)
    set_line(level1, Pair(10,0), Pair(10, 5), block, window.width / 15, window.width / 15)

    return level1
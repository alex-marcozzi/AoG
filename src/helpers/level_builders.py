import pyglet
from src.helpers.utils import block_width
from src.entity import Entity
from src.entity_classes.character import Character
from src.entity_classes.bear import Bear
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

def set_bear(level_array: list, pos: Pair, window, block_w):
    x = pos.first
    y = pos.second
    bear = Bear(window)
    bear.global_pos = Pair(x * block_w, y * block_w)
    print(f"TYPE: {type(bear)}")
    level_array[pos.first][pos.second] = bear


def build_level1(window):
    block_w = block_width(window)
    block = Entity(window, "assets/images/orange.png", global_pos=Pair(0, 0), velocity=Pair(0,0), acceleration=Pair(0,0), width=window.width / 15, height = window.width / 15)
    bear = Bear(window)
    level1 = initialize_level_base(100, 100)
    set_line(level1, Pair(0,2), Pair(30, 2), block, block_w, block_w)
    # set_line(level1, Pair(15,2), Pair(15, 3), block, block_w, block_w)
    set_line(level1, Pair(30,2), Pair(30, 3), block, block_w, block_w)
    set_line(level1, Pair(32,3), Pair(40, 3), block, block_w, block_w)
    
    set_bear(level1, Pair(20, 3), window, block_w)

    return level1
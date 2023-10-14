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
def set_line(
    level_array: list, from_pos: Pair, to_pos: Pair, entity: Entity, block_w, block_h
):
    for x in range(from_pos.first, to_pos.first + 1):
        for y in range(from_pos.second, to_pos.second + 1):
            this_entity = entity.copy()
            this_entity.global_pos = Pair(x * block_w, y * block_h)
            level_array[x][y] = this_entity


def set_bear(level_array: list, pos: Pair, window, block_w, batch):
    global_pos = Pair(pos.first * block_w, pos.second * block_w)
    bear = Bear(window, global_pos, batch)
    level_array[pos.first][pos.second] = bear


def build_level1(window, batch):
    block_w = block_width(window)
    block = Entity(
        window,
        "assets/images/bbox.png",
        global_pos=Pair(0, 0),
        velocity=Pair(0, 0),
        acceleration=Pair(0, 0),
        sprite_width=window.width / 15,
        sprite_height=window.width / 15,
        hitbox_width=block_w,
        hitbox_height=block_w,
        batch=batch,
    )
    level1 = initialize_level_base(100, 100)
    set_line(level1, Pair(0, 2), Pair(30, 2), block, block_w, block_w)
    set_line(level1, Pair(12, 2), Pair(12, 3), block, block_w, block_w)
    set_line(level1, Pair(30, 2), Pair(30, 3), block, block_w, block_w)
    set_line(level1, Pair(32, 3), Pair(40, 3), block, block_w, block_w)
    set_line(level1, Pair(34, 6), Pair(36, 6), block, block_w, block_w)
    set_line(level1, Pair(42, 5), Pair(50, 5), block, block_w, block_w)

    # set_bear(level1, Pair(10, 3), window, block_w, batch)
    # set_bear(level1, Pair(13, 3), window, block_w, batch)
    set_bear(level1, Pair(16, 3), window, block_w, batch)
    # set_bear(level1, Pair(19, 3), window, block_w, batch)
    # set_bear(level1, Pair(24, 3), window, block_w, batch)

    return level1

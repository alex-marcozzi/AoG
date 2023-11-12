import pyglet
from src.helpers.utils import block_width, make_sprite
from src.entity import Entity
from src.entity_classes.character import Character
from src.entity_classes.character_classes.bear import Bear
from src.helpers.interfaces import Pair
from src.sprite_collection import SpriteCollection
from src.entity_classes.block_classes.standard_block import StandardBlock
from src.entity_classes.block_classes.moving_block import MovingBlock
from src.entity_classes.pickup_classes.wizard_pickup import WizardPickup
from src.entity_classes.pickup import Pickup


def initialize_level_base(x_width, y_height):
    return [[None for col in range(x_width)] for row in range(y_height)]


# sets the squares in "level_array" specified in a line from "from_pos" to "to_pos" to the "entity" object
# note: inclusive beginning, inclusive end
# def set_line(
#     level_array: list, from_pos: Pair, to_pos: Pair, entity: Entity, block_w, block_h
# ):
#     for x in range(from_pos.first, to_pos.first + 1):
#         for y in range(from_pos.second, to_pos.second + 1):
#             this_entity = entity.copy()
#             this_entity.global_pos = Pair(x * block_w, y * block_h)
#             level_array[x][y] = this_entity

def set_line(level_array: list, from_pos: Pair, to_pos: Pair, window, block_w: float, batch):
    for x in range(from_pos.first, to_pos.first + 1):
        for y in range(from_pos.second, to_pos.second + 1):
            set_block(level_array, pos=Pair(x, y), window=window, block_w=block_w, batch=batch)

def set_wizard_pickup(level_array: list, pos: Pair, window, block_w, batch):
    global_pos = Pair(pos.first * block_w, pos.second * block_w)
    bear = WizardPickup(window, global_pos, batch)
    level_array[pos.first][pos.second] = bear

def set_bear(level_array: list, pos: Pair, window, block_w, batch):
    global_pos = Pair(pos.first * block_w, pos.second * block_w)
    bear = Bear(window, global_pos, batch)
    level_array[pos.first][pos.second] = bear

def set_block(level_array: list, pos: Pair, window, block_w, batch):
    global_pos = Pair(pos.first * block_w, pos.second * block_w)
    block = StandardBlock(window, global_pos, batch)
    level_array[pos.first][pos.second] = block

def set_moving_block(level_array: list, pos: Pair, window, block_w, batch, start_right: bool = False):
    global_pos = Pair(pos.first * block_w, pos.second * block_w)
    block = MovingBlock(window, global_pos, 10, 3, batch, start_right)
    # block.id = 999
    level_array[pos.first][pos.second] = block


def build_level1(window, batch):
    block_w = block_width(window)
    sprites = SpriteCollection(idle_right=make_sprite(sprite_filename="assets/images/bbox.png",
                                                      width=block_w,
                                                      height=block_w,
                                                      visible=True,
                                                      batch=batch),
                                idle_left=make_sprite(sprite_filename="assets/images/bbox.png",
                                                      width=block_w,
                                                      height=block_w,
                                                      visible=True,
                                                      batch=batch))
    
    level1 = initialize_level_base(100, 100)
    set_line(level1, Pair(0, 2), Pair(30, 2), window, block_w, batch)
    set_line(level1, Pair(7, 5), Pair(8, 5), window, block_w, batch)
    set_moving_block(level1, Pair(10, 7), window, block_w, batch, False)
    # set_moving_block(level1, Pair(10, 10), window, block_w, batch, True)
    set_line(level1, Pair(12, 2), Pair(12, 3), window, block_w, batch)
    set_line(level1, Pair(30, 2), Pair(30, 3), window, block_w, batch)
    set_line(level1, Pair(33, 3), Pair(40, 3), window, block_w, batch)
    set_line(level1, Pair(34, 6), Pair(36, 6), window, block_w, batch)
    set_line(level1, Pair(42, 5), Pair(50, 5), window, block_w, batch)

    # set_bear(level1, Pair(10, 3), window, block_w, batch)
    # set_bear(level1, Pair(13, 3), window, block_w, batch)
    set_bear(level1, Pair(16, 3), window, block_w, batch)
    # set_bear(level1, Pair(19, 3), window, block_w, batch)
    # set_bear(level1, Pair(24, 3), window, block_w, batch)

    set_wizard_pickup(level1, Pair(11, 3), window, block_w, batch)

    return level1

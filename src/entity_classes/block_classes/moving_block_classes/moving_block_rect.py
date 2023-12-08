import pyglet
from src.helpers.utils import std_speed, block_width, gravity, make_sprite
from src.helpers.interfaces import Pair
from src.helpers.context import Context
from src.entity_classes.block_classes.moving_block import MovingBlock

# block that moves in a rectangle pattern
class MovingBlockRect(MovingBlock):
    
    def __init__(self, context: Context, block_pos: Pair, width, height, cycle_time: float = 5, starting_pivot: int = 0, clockwise: bool = False):
        if clockwise:
            pivots = [
                block_pos,
                Pair(block_pos.first, block_pos.second + height),
                Pair(block_pos.first + width, block_pos.second + height),
                Pair(block_pos.first + width, block_pos.second)
            ]
        else:
            pivots = [
                block_pos,
                Pair(block_pos.first + width, block_pos.second),
                Pair(block_pos.first + width, block_pos.second + height),
                Pair(block_pos.first, block_pos.second + height),
            ]

        times = [
            cycle_time / 4.0,
            cycle_time / 4.0,
            cycle_time / 4.0,
            cycle_time / 4.0,
        ]

        super().__init__(
            context=context,
            pivots=pivots,
            times=times,
            starting_pivot=starting_pivot,
        )
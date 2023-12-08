import pyglet
from src.helpers.utils import std_speed, block_width, gravity, make_sprite
from src.helpers.interfaces import Pair
from src.helpers.context import Context
from src.entity_classes.block_classes.moving_block import MovingBlock

# block that moves in a vertical line
class MovingBlockVLine(MovingBlock):
    
    def __init__(self, context: Context, block_pos, dist, cycle_time: float = 5, starting_pivot: int = 0):
        pivots = [
            block_pos,
            Pair(block_pos.first, block_pos.second + dist)
        ]
        times = [
            cycle_time / 2.0,
            cycle_time / 2.0
        ]


        super().__init__(
            context=context,
            pivots=pivots,
            times=times,
            starting_pivot=starting_pivot,
        )
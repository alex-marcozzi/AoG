import pyglet
from src.helpers.utils import std_speed, block_width, gravity, make_sprite
from src.helpers.interfaces import Pair
from src.entity_classes.block_classes.moving_block import MovingBlock

# block that moves in a horizontal line
class MovingBlockVLine(MovingBlock):
    
    def __init__(self, window, batch, block_pos, dist, cycle_time: float = 5,starting_pivot: int = 0):
        self.block_w = block_width(window)
        print(block_pos)
        pivots = [
            block_pos,
            Pair(block_pos.first, block_pos.second + dist)
        ]
        times = [
            cycle_time / 2.0,
            cycle_time / 2.0
        ]

        print(cycle_time)

        super().__init__(
            window=window,
            pivots=pivots,
            times=times,
            batch=batch,
            starting_pivot=starting_pivot,
        )
import pyglet
from src.helpers.utils import std_speed, block_width, gravity, make_sprite, float_eq_pair
from src.helpers.interfaces import Pair
from src.entity import Entity
from src.sprite_collection import SpriteCollection
from src.entity_classes.block import Block
from src.helpers.globals import Direction
import time


class MovingBlock(Block):
    # a pivot is a block_pos where the moving block will change course once it is reached
    # ex: a block moving in a square would have four pivots, one in each corner
    def __init__(self, window, pivots: list[Pair], times: list[float], batch, starting_pivot: int = 0):
        sprites = SpriteCollection(idle_right=make_sprite(sprite_filename="assets/images/bbox.png",
                                                    width=block_width(window) * 2,
                                                    height=block_width(window),
                                                    visible=True,
                                                    batch=batch),
                                    idle_left=make_sprite(sprite_filename="assets/images/bbox.png",
                                                    width=block_width(window) * 2,
                                                    height=block_width(window),
                                                    visible=False,
                                                    batch=batch),)
        self.block_w = block_width(window)
        self.pivots = pivots
        global_pos = Pair(self.block_w * pivots[starting_pivot].first, self.block_w * pivots[starting_pivot].second)
        self.times = times

        super().__init__(
            window=window,
            sprites=sprites,
            global_pos=global_pos,
            hitbox_width=block_width(window) * 2,
            hitbox_height=block_width(window),
            batch=batch,
        )

        self.current = starting_pivot
        self.next()

        # self.speed = (block_width(window) * distance) / time  # we want to move one block per second
        # self.starting_block_pos = self.block_pos
        # self.time = time
        # self.distance = distance
        # self.start_right = start_right

        # if start_right:
        #     self.global_pos.first += distance * block_width(window)
        #     self.direction = Direction.LEFT

    def copy(self):
        new_copy = MovingBlock(window=self.window,
                             pivots=self.pivots.copy(),
                             batch=self.batch,
                             starting_pivot=self.current)
        
        return new_copy
    
    def next(self):
        print("SNAP****************************************************************************************************************")
        self.current = (self.current + 1) % len(self.pivots)

        dist_x = (self.block_w * self.pivots[self.current].first) - self.global_pos.first
        dist_y = (self.block_w * self.pivots[self.current].second) - self.global_pos.second
        # self.velocity = Pair(0, 0)
        self.velocity = Pair(dist_x / self.times[self.current], dist_y / self.times[self.current])

    def reached_pivot(self):
        target_pos = Pair(self.block_w * self.pivots[self.current].first, self.block_w * self.pivots[self.current].second)

        return float_eq_pair(self.global_pos, target_pos, self.block_w / 4)
    
    def pre_tick(self, dt: float):
        pass
        # if self.reached_pivot():
        #     self.next()
        # self.calculate_velocity()
        # if self.velocity.first > 0:
        #     self.direction = Direction.RIGHT
        # elif self.velocity.first < 0:
        #     self.direction = Direction.LEFT

    def tick(self, dt: float, camera_pos: Pair):
        super().tick(dt, camera_pos)
        if self.reached_pivot():
            self.next()

        # if self.direction == Direction.RIGHT and self.block_pos.first - self.starting_block_pos.first >= self.distance:
        #     self.direction = Direction.LEFT
        # elif self.direction == Direction.LEFT and self.block_pos.first - self.starting_block_pos.first <= 0:
        #     self.direction = Direction.RIGHT
    
    def calculate_velocity(self):
        self.velocity = Pair(0, 0)
        # self.velocity = Pair(0, self.velocity.second)
        # speed = self.get_speed()
        # # print(speed)
        # self.velocity = Pair(self.velocity.first + speed, self.velocity.second)
    
    def get_speed(self):
        speed = self.speed
        if self.direction == Direction.LEFT:
            speed = -1 * speed
        
        return speed
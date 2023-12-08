import pyglet
from src.helpers.utils import std_speed, block_width, gravity, make_sprite
from src.helpers.interfaces import Pair
from src.helpers.context import Context
from src.entity import Entity
from src.sprite_collection import SpriteCollection
from src.entity_classes.block import Block
from src.helpers.globals import Direction
import time


class StandardBlock(Block):
    def __init__(self, context: Context, global_pos):
        sprites = SpriteCollection(idle_right=make_sprite(sprite_filename="assets/images/bbox.png",
                                                    width=context.block_w,
                                                    height=context.block_w,
                                                    visible=True,
                                                    batch=context.batch),
                                    idle_left=make_sprite(sprite_filename="assets/images/bbox.png",
                                                    width=context.block_w,
                                                    height=context.block_w,
                                                    visible=False,
                                                    batch=context.batch),)
        super().__init__(
            context=context,
            sprites=sprites,
            global_pos=global_pos,
            hitbox_width=context.block_w,
            hitbox_height=context.block_w,
        )

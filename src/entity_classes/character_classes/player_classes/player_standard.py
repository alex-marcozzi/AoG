import pyglet
from src.helpers.utils import block_width, std_speed, make_sprite, gravity
from src.helpers.interfaces import Pair
from src.helpers.context import Context
from src.entity import Entity
from src.attack import Attack
from src.hitbox import Hitbox
from src.sprite_collection import SpriteCollection
from src.entity_classes.character import Character
from src.entity_classes.projectile_classes.lightning import Lightning
from src.entity_classes.character_classes.player import Player
from src.helpers.globals import Direction
import time


class PlayerStandard(Player):
    def __init__(
        self,
        context: Context,
        global_pos: Pair,
        # keys_down,
        # keys_usable,
    ):
        idle_width = context.block_w
        sprites = SpriteCollection(idle_right=make_sprite(sprite_filename="assets/images/sprites/goose_default/idle_right.png",
                                                    width=idle_width,
                                                    height=context.block_w,
                                                    visible=True,
                                                    batch=context.batch),
                                    idle_left=make_sprite(sprite_filename="assets/images/sprites/goose_default/idle_left.png",
                                                    width=idle_width,
                                                    height=context.block_w,
                                                    visible=False,
                                                    batch=context.batch),
                                    damaged_right=make_sprite(sprite_filename="assets/images/orange.png",
                                                    width=idle_width,
                                                    height=context.block_w,
                                                    visible=False,
                                                    batch=context.batch),
                                    damaged_left=make_sprite(sprite_filename="assets/images/orange.png",
                                                    width=idle_width,
                                                    height=context.block_w,
                                                    visible=False,
                                                    batch=context.batch),)
        super().__init__(
            context,
            sprites,
            global_pos,
            context.block_w,
            context.block_w,
            hp=3,
        )

        self.flicker_filename = "assets/images/sprites/goose_default/idle_right.png"
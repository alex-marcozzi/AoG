import pyglet
from src.helpers.utils import block_width, std_speed, make_sprite, gravity
from src.helpers.interfaces import Pair
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
        window,
        global_pos: Pair,
        batch,
    ):
        idle_width = block_width(window)
        sprites = SpriteCollection(idle_right=make_sprite(sprite_filename="assets/images/sprites/goose_default/idle_right.png",
                                                    width=idle_width,
                                                    height=block_width(window),
                                                    visible=True,
                                                    batch=batch),
                                    idle_left=make_sprite(sprite_filename="assets/images/sprites/goose_default/idle_left.png",
                                                    width=idle_width,
                                                    height=block_width(window),
                                                    visible=False,
                                                    batch=batch),
                                    damaged_right=make_sprite(sprite_filename="assets/images/orange.png",
                                                    width=idle_width,
                                                    height=block_width(window),
                                                    visible=False,
                                                    batch=batch),
                                    damaged_left=make_sprite(sprite_filename="assets/images/orange.png",
                                                    width=idle_width,
                                                    height=block_width(window),
                                                    visible=False,
                                                    batch=batch),)
        super().__init__(
            window,
            sprites,
            global_pos,
            block_width(window),
            block_width(window),
            batch,
            hp=3,
        )

        self.flicker_filename = "assets/images/sprites/goose_default/idle_right.png"
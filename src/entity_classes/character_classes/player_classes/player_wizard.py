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


class PlayerWizard(Player):
    def __init__(
        self,
        context: Context,
        global_pos: Pair,
    ):
        idle_width = context.block_w
        attack = Attack(
                range=context.block_w,
                duration=0.1,
                damage=1,
                cooldown=0.10,
                projectiles=[Lightning(context=context, global_pos=Pair(0, 0), angle=0),]
                            #  Lightning(window=window, global_pos=Pair(0, 0), angle=45, batch=batch),
                            #  Lightning(window=window, global_pos=Pair(0, 0), angle=22.5, batch=batch),
                            #  Lightning(window=window, global_pos=Pair(0, 0), angle=-45, batch=batch),
                            #  Lightning(window=window, global_pos=Pair(0, 0), angle=-22.5, batch=batch),]
            )
        sprites = SpriteCollection(idle_right=make_sprite(sprite_filename="assets/images/wizard_pickup.png",
                                                    width=idle_width,
                                                    height=context.block_w,
                                                    visible=True,
                                                    batch=context.batch),
                                    idle_left=make_sprite(sprite_filename="assets/images/wizard_pickup.png",
                                                    width=idle_width,
                                                    height=context.block_w,
                                                    visible=False,
                                                    batch=context.batch),
                                    attack_right=make_sprite(sprite_filename="assets/images/sprites/goose_default/idle_right.png",
                                                    width=idle_width + attack.range,
                                                    height=context.block_w,
                                                    visible=False,
                                                    batch=context.batch),
                                    attack_left=make_sprite(sprite_filename="assets/images/sprites/goose_default/idle_left.png",
                                                    width=idle_width + attack.range,
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
            hp=5,
            attack=attack,
        )

        self.max_jumps = 3
        self.num_jumps = self.max_jumps
        self.flicker_filename = "assets/images/sprites/goose_default/idle_left.png"

    def tick(self, dt: float, camera_pos: Pair):
        if self.on_ground:
            self.num_jumps = self.max_jumps
        super().tick(dt, camera_pos)

    def check_keys(self):
        super().check_keys()
        if self.context.keys_down.get(pyglet.window.key.SPACE, False) and self.num_jumps > 0 and not self.on_ground:
            self.jump(0.80)
            self.num_jumps -= 1
            self.context.keys_down[pyglet.window.key.SPACE] = False
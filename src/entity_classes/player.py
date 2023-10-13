import pyglet
from src.helpers.utils import block_width, std_speed, make_sprite, gravity
from src.helpers.interfaces import Pair
from src.entity import Entity
from src.attack import Attack
from src.hitbox import Hitbox
from src.SpriteCollection import SpriteCollection
from src.entity_classes.character import Character
from src.helpers.globals import Direction
import time


class Player(Character):
    def __init__(
        self,
        window,
        sprite_filename: str,
        global_pos: Pair,
        velocity: Pair,
        acceleration: Pair,
        sprite_width: float,
        sprite_height: float,
        hitbox_width: float,
        hitbox_height: float,
        batch,
    ):
        sprites = SpriteCollection(idle=make_sprite(sprite_filename="assets/images/goose.png",
                                                    width=block_width(window),
                                                    height=block_width(window),
                                                    visible=True,
                                                    batch=batch),
                                    attack=make_sprite(sprite_filename="assets/images/goose.png",
                                                    width=block_width(window) * 2,
                                                    height=block_width(window),
                                                    visible=False,
                                                    batch=batch),)
        super().__init__(
            window,
            sprites,
            global_pos,
            velocity,
            Pair(0, gravity(window)), #acceleration,
            hitbox_width,
            hitbox_height,
            batch,
            hp=3,
            attack=Attack(
                hitboxes=[
                    Hitbox(pos=Pair(0, 0), width=hitbox_width * 2, height=hitbox_height)
                ],
                duration=0.1,
                damage=1,
                cooldown=0.10,
            ),
            # attack_sprite_filename="assets/images/goose.png"
        )

        # self.standard_speed = std_speed(window)
        self.keys_down = {}
        self.keys_usable = {}
        self.modifiers = []

    def pre_tick(self, dt: float):
        super().pre_tick(dt)
        self.check_keys()

    # def tick(self, camera_pos: Pair):
    #     super().tick(camera_pos)

    def interact(self, entity: Entity, direction):
        if "collidable" in entity.modifiers:
            self.interact_collidable(entity, direction)
            if direction == Direction.DOWN:
                self.keys_usable[pyglet.window.key.SPACE] = True
        if "dangerous" in entity.modifiers:
            self.interact_dangerous(entity, direction)

    def handle_key_press(self, symbol, modifiers):
        self.keys_down[symbol] = True

    def handle_key_release(self, symbol, modifiers):
        self.keys_down[symbol] = False

    def check_keys(self):
        # if self.can_move():
            if self.keys_down.get(pyglet.window.key.A, False):
                self.velocity = Pair(
                    self.velocity.first - self.standard_speed, self.velocity.second
                )
            if self.keys_down.get(pyglet.window.key.D, False):
                self.velocity = Pair(
                    self.velocity.first + self.standard_speed, self.velocity.second
                )
            if self.keys_down.get(pyglet.window.key.SPACE, False) and self.on_ground:
                self.velocity = Pair(
                    self.velocity.first, self.velocity.second + (self.standard_speed * 1.3) #(self.block_w / 5)
                )
            if self.keys_down.get(pyglet.window.key.F, False) and self.attack.isUsable():# and not self.attack.inProgress():
                print(">> THROWING ATTACK")
                self.attack.Throw()

    def can_move(self):
        if self.attack.inProgress():
            return False
        
        return True
import pyglet
from src.helpers.utils import std_speed, block_width, gravity, make_sprite
from src.helpers.interfaces import Pair
from src.helpers.context import Context
from src.entity import Entity
from src.sprite_collection import SpriteCollection
from src.entity_classes.character import Character
from src.helpers.globals import Direction
from src.attack import Attack
from src.entity_classes.projectile_classes.lightning import Lightning
import time


class Bear(Character):
    def __init__(self, context: Context, global_pos):
        self.speed = context.std_speed / 2
        attack = Attack(
                range=context.block_w,
                duration=0.1,
                damage=1,
                cooldown=0.10,
                # projectiles=[Lightning(window=window, global_pos=Pair(0, 0), angle=0, batch=batch),]
                            #  Lightning(window=window, global_pos=Pair(0, 0), angle=45, batch=batch),
                            #  Lightning(window=window, global_pos=Pair(0, 0), angle=22.5, batch=batch),
                            #  Lightning(window=window, global_pos=Pair(0, 0), angle=-45, batch=batch),
                            #  Lightning(window=window, global_pos=Pair(0, 0), angle=-22.5, batch=batch),]
            )

        idle_width = context.block_w * 2
        sprites = SpriteCollection(idle_right=make_sprite(sprite_filename="assets/images/bear.png",
                                                    width=idle_width,
                                                    height=context.block_w * 2,
                                                    visible=True,
                                                    batch=context.batch),
                                    idle_left=make_sprite(sprite_filename="assets/images/bear.png",
                                                    width=idle_width,
                                                    height=context.block_w * 2,
                                                    visible=False,
                                                    batch=context.batch),
                                    attack_right=make_sprite(sprite_filename="assets/images/bear.png",
                                                    width=idle_width + attack.range,
                                                    height=context.block_w * 2,
                                                    visible=False,
                                                    batch=context.batch),
                                    attack_left=make_sprite(sprite_filename="assets/images/bear.png",
                                                    width=idle_width + attack.range,
                                                    height=context.block_w * 2,
                                                    visible=False,
                                                    batch=context.batch),
                                    damaged_right=make_sprite(sprite_filename="assets/images/orange.png",
                                                    width=idle_width,
                                                    height=context.block_w * 2,
                                                    visible=False,
                                                    batch=context.batch),
                                    damaged_left=make_sprite(sprite_filename="assets/images/orange.png",
                                                    width=idle_width,
                                                    height=context.block_w * 2,
                                                    visible=False,
                                                    batch=context.batch),)
        super().__init__(
            context=context,
            sprites=sprites,
            global_pos=global_pos,
            hitbox_width=context.block_w * 2,
            hitbox_height=context.block_w * 2,
            hp=3,
            attack=attack
        )

        self.modifiers = ["dangerous", "bouncy", "vulnerable_top"]#, "collidable"]
        self.move_loop_start = time.time()
        # self.left = True
        self.direction = Direction.LEFT
        self.flicker_filename = "assets/images/bear.png"
        # pyglet.clock.schedule_interval(self.attack.Throw, interval=1.5)  # update at 60Hz

    # def pre_tick(self, dt: float):
    #     super().pre_tick(dt)
        # self.calculate_velocity()

    # def tick(self, camera_pos: Pair):
    #     super().tick(camera_pos)
    #     self.velocity = Pair(self.velocity.first - self.speed, self.velocity.second)
    
    def calculate_velocity(self):
        super().calculate_velocity()
        speed = self.get_speed()
        # print(speed)
        self.velocity = Pair(self.velocity.first + speed, self.velocity.second)

    def interact(self, entity: Entity, direction):
        if direction == Direction.LEFT:
            self.direction = Direction.RIGHT
        elif direction == Direction.RIGHT:
            self.direction = Direction.LEFT
        if "collidable" in entity.modifiers:
            self.interact_collidable(entity, direction)
        # if "dangerous" in entity.modifiers:
        #     self.interact_dangerous(entity, direction)


    # function: y = 1 - (2x - 1)^2
    # x: time
    # y: speed
    def get_speed(self):
        speed = self.speed
        if self.direction == Direction.LEFT:
            speed = -1 * speed
        
        return speed
        # now = time.time()
        # x = (now - self.move_loop_start) / 3.0
        # y = 1 - (((2 * x) - 1) ** 2)
        # y *= -1 if self.left else 1

        # if x >= 1:
        #     self.move_loop_start = now
        #     self.left = not self.left

        # return y

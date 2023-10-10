import pyglet
from src.helpers.utils import std_speed, block_width
from src.helpers.interfaces import Pair
from src.entity import Entity
from src.attack import Attack
from src.helpers.globals import Direction
import time

loaded_images = {}  # key: filename, value: image

class Character(Entity):
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
        hp: int,
        attack: Attack = None,
        attack_sprite_filename: str = None,
    ):
        super().__init__(
            window,
            sprite_filename,
            global_pos,
            velocity,
            acceleration,
            sprite_width,
            sprite_height,
            hitbox_width,
            hitbox_height,
            batch,
        )

        self.hp = hp
        self.width_in_blocks = hitbox_width // block_width(window)
        # self.standard_speed = std_speed(window)
        # self.block_below = None
        self.on_ground = False
        self.immunity_start = time.time()
        self.immunity_duration_seconds = 1
        self.attack = attack
        
        self.attack_sprite_filename = attack_sprite_filename
        if attack_sprite_filename:
            if not attack_sprite_filename in loaded_images.keys():
                loaded_images[attack_sprite_filename] = pyglet.resource.image(attack_sprite_filename)
            self.attack_sprite = pyglet.sprite.Sprite(
                img=loaded_images[attack_sprite_filename], batch=batch
            )
            self.attack_sprite.width = self.attack.hitboxes[0].width
            self.attack_sprite.height = self.attack.hitboxes[0].height
            self.attack_sprite.visible = False

    def pre_tick(self):
        self.velocity = Pair(0, self.velocity.second)
        # self.check_keys()
        # self.player.check_keys()

    def tick(self, camera_pos: Pair):
        super().tick(camera_pos)
        if self.attack:
            if self.attack.inProgress():
                self.sprite.visible = False
                self.attack_sprite.visible = True
                # if self.current_sprite_filename != self.attack_sprite_filename:
                #     if not self.attack_sprite_filename in loaded_images.keys():
                #         loaded_images[self.attack_sprite_filename] = pyglet.resource.image(self.attack_sprite_filename)
                #     self.sprite.image = loaded_images[self.attack_sprite_filename]
                #     self.current_sprite_filename = self.attack_sprite_filename
                #     self.sprite.width = self.attack.hitboxes[0].width
                #     self.sprite.height = self.attack.hitboxes[0].height
                #     self.sprite.visible = False

                # self.attack_sprite.draw()
            else:
                self.sprite.visible = True
                self.attack_sprite.visible = False

        
        if self.attack_sprite_filename:
            self.attack_sprite.x = self.global_pos.first - (
                camera_pos.first - (self.window.width / 2)
            )
            self.attack_sprite.y = self.global_pos.second - (
                camera_pos.second - (self.window.height / 2)
            )

        if self.hp <= 0:
            return False

        return True
    
    # def draw(self):
    #     if self.attack and self.attack.inProgress():
    #         self.attack_sprite.draw()
    #     else:
    #         super().draw()

    def interact(self, entity: Entity, direction):
        if "collidable" in entity.modifiers:
            self.interact_collidable(entity, direction)

    def interact_collidable(self, entity: Entity, direction):
        if direction == Direction.DOWN:
            self.global_pos = Pair(
                self.global_pos.first, entity.global_pos.second + entity.sprite.height
            )
            self.velocity = Pair(self.velocity.first + entity.velocity.first, 0)
        #     self.on_ground = True
        # else:
        #     self.on_ground = False
        if direction == Direction.RIGHT:
            if (
                not issubclass(type(entity), Character)
                and self.block_pos.second - 1 == entity.block_pos.second
            ):
                return
            print("! RIGHT COLLISION")
            self.global_pos = Pair(
                entity.global_pos.first - self.hitbox.width, self.global_pos.second
            )
            self.velocity = Pair(0, self.velocity.second)
        if direction == Direction.LEFT:
            if (
                not issubclass(type(entity), Character)
                and self.block_pos.second - 1 == entity.block_pos.second
            ):
                return
            print("! LEFT COLLISION")
            self.global_pos = Pair(
                entity.global_pos.first + entity.hitbox.width, self.global_pos.second
            )
            self.velocity = Pair(0, self.velocity.second)
        if direction == Direction.UP:
            print("! UP COLLISION")
            self.global_pos = Pair(
                self.global_pos.first, entity.global_pos.second - self.sprite.height
            )
            self.velocity = Pair(self.velocity.first, 0)

    def interact_dangerous(self, entity: Entity, direction):
        now = time.time()
        if (
            direction == Direction.OVERLAP
            and now - self.immunity_start > self.immunity_duration_seconds
        ):
            print("DANGER DANGER DANGER")
            self.takeDamage(1)

    def takeDamage(self, amount):
        self.hp = max(self.hp - amount, 0)
        self.immunity_start = time.time()  # epoch time

    def takeHit(self, attack: Attack):
        # when we add modifiers later we could do checking here:
        # if "poisonous" in self.modifiers:
        #       etc.

        self.takeDamage(amount=attack.damage)

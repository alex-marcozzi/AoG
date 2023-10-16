import pyglet
from src.helpers.interfaces import Pair
from src.helpers.utils import block_width, std_speed, make_sprite
from src.helpers.globals import Direction
from src.hitbox import Hitbox
from src.sprite_collection import SpriteCollection
import uuid

# loaded_images = {}  # key: filename, value: image


class Entity:
    def __init__(
        self,
        window,
        sprites: SpriteCollection,
        global_pos: Pair,
        hitbox_width: float,
        hitbox_height: float,
        batch=None,
        velocity=None,
        acceleration=None,
    ):
        self.window = window
        self.standard_speed = std_speed(window)
        self.block_w = block_width(window)
        self.batch = batch
        self.sprites = sprites
        self.hitbox = Hitbox(pos=global_pos, width=hitbox_width, height=hitbox_height)
        self.global_pos = global_pos.copy()
        self.block_pos = Pair(
            self.global_pos.first // self.block_w,
            (self.global_pos.second + 10) // self.block_w,
        )
        self.velocity = velocity if velocity else Pair(0, 0)
        self.acceleration = acceleration if acceleration else Pair(0, 0)
        self.modifiers = ["collidable"]
        self.direction = Direction.RIGHT
        self.id = uuid.uuid1()

    def copy(self):
        new_copy = Entity(
            window=self.window,
            sprites=self.sprites.copy(),
            global_pos=self.global_pos,
            sprite_width=self.sprites.idle_right.width,
            sprite_height=self.sprites.idle_right.height,
            hitbox_width=self.hitbox.width,
            hitbox_height=self.hitbox.height,
            batch=self.batch,
            velocity=self.velocity,
            acceleration=self.acceleration,
        )
        return new_copy

    def tick_pos_only(self, dt: float):
        self.global_pos.add(Pair(self.velocity.first * dt, self.velocity.second * dt))
        # self.velocity.add(self.acceleration)

    def tick(self, dt: float, camera_pos: Pair):
        self.global_pos.add(Pair(self.velocity.first * dt, self.velocity.second * dt))
        self.velocity.add(Pair(self.acceleration.first * dt, self.acceleration.second * dt))
        # self.global_pos.add

        # camera_pos == player.global_pos (middle of screen)
        # if self.sprites:
        #     self.sprites.idle_right.x = self.global_pos.first - (
        #         camera_pos.first - (self.window.width / 2)
        #     )
        #     self.sprites.idle_right.x = self.global_pos.second - (
        #         camera_pos.second - (self.window.height / 2)
        #     )
        self.block_pos = Pair(
            self.global_pos.first // self.block_w,
            (self.global_pos.second + 10) // self.block_w,
        )
        self.hitbox.pos = self.global_pos.copy()

        self.update_sprite_positions(camera_pos)
        self.update_current_sprite()

    # def draw(self):
    #     self.sprite.draw()

    def update_sprite_positions(self, camera_pos: Pair):
        self.sprites.idle_right.x = self.global_pos.first - (
            camera_pos.first - (self.window.width / 2) - ((self.hitbox.width - self.sprites.idle_right.width) / 2)
        )
        self.sprites.idle_right.y = self.global_pos.second - (
            camera_pos.second - (self.window.height / 2)
        )
        self.sprites.idle_left.x = self.sprites.idle_right.x
        self.sprites.idle_left.y = self.sprites.idle_right.y
        
        if self.sprites.slow_move_right:
            self.sprites.slow_move_right.x = self.sprites.idle_right.x
            self.sprites.slow_move_right.y = self.sprites.idle_right.y
        
        if self.sprites.slow_move_left:
            self.sprites.slow_move_left.x = self.sprites.idle_right.x
            self.sprites.slow_move_left.y = self.sprites.idle_right.y
        
        if self.sprites.fast_move_right:
            self.sprites.fast_move_right.x = self.sprites.idle_right.x
            self.sprites.fast_move_right.y = self.sprites.idle_right.y
        
        if self.sprites.fast_move_left:
            self.sprites.fast_move_left.x = self.sprites.idle_right.x
            self.sprites.fast_move_left.y = self.sprites.idle_right.y
        
        # if self.sprites.attack_right:
        #     self.sprites.attack_right.x = self.sprites.idle_right.x
        #     self.sprites.attack_right.y = self.sprites.idle_right.y
        
        # if self.sprites.attack_left:
        #     self.sprites.attack_left.x = self.sprites.idle_right.x - self.attack.range
        #     self.sprites.attack_left.y = self.sprites.idle_right.y
        
        if self.sprites.damaged_right:
            self.sprites.damaged_right.x = self.sprites.idle_right.x
            self.sprites.damaged_right.y = self.sprites.idle_right.y
        
        if self.sprites.damaged_left:
            self.sprites.damaged_left.x = self.sprites.idle_right.x
            self.sprites.damaged_left.y = self.sprites.idle_right.y
    
    def update_current_sprite(self):
        if self.direction == Direction.RIGHT:
            self.sprites.SetVisible(self.sprites.idle_right)
        elif self.direction == Direction.LEFT:
            self.sprites.SetVisible(self.sprites.idle_left)
        self.sprites.SetVisible(self.sprites.idle_right)


    def interact(self, entity: "Entity", direction):
        if "collidable" in entity.modifiers:
            if direction == Direction.DOWN:
                self.global_pos = Pair(
                    self.global_pos.first,
                    entity.global_pos.second + entity.sprite.height,
                )
                self.velocity = Pair(self.velocity.first, 0)

        pass

    def nextPos(self):
        return Pair(
            self.global_pos.first + self.velocity.first,
            self.global_pos.second + self.velocity.second,
        )

    def bottomLeft(self):
        return self.global_pos

    def bottomRight(self):
        return Pair(self.global_pos.first + self.hitbox.width, self.global_pos.second)

    def topLeft(self):
        return Pair(self.global_pos.first, self.global_pos.second + self.hitbox.height)

    def topRight(self):
        return Pair(
            self.global_pos.first + self.hitbox.width,
            self.global_pos.second + self.hitbox.height,
        )

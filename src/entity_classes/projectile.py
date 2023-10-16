import pyglet
from src.helpers.utils import std_speed, block_width, make_sprite, distance
from src.helpers.interfaces import Pair
from src.entity import Entity
from src.sprite_collection import SpriteCollection
from src.helpers.globals import Direction

class Projectile(Entity):
    def __init__(
        self,
        window,
        sprites: SpriteCollection,
        global_pos: Pair,
        velocity: Pair,
        acceleration: Pair,
        range: float,
        hitbox_width: float,
        hitbox_height: float,
        batch,
    ):
        # self.sprites = SpriteCollection(idle=self.sprite)
        self.sprites = sprites
        # self.sprites.SetVisible(self.sprites.idle_right)
        self.sprites.SetAllInvisible()
        
        super().__init__(
            window,
            sprites,
            global_pos,
            velocity,
            acceleration,
            None,
            None,
            hitbox_width,
            hitbox_height,
            batch,
        )
        self.direction = Direction.RIGHT
        self.modifiers = ["dangerous"]
        self.range = range
        self.spawn_pos = None

    def copy(self):
        new_copy = Projectile(window=self.window,
                             sprites=self.sprites.copy(),
                             global_pos=self.global_pos,
                             velocity=self.velocity,
                             acceleration=self.acceleration,
                             hitbox_width=self.hitbox.width,
                             hitbox_height=self.hitbox.height,
                             batch=self.batch,)
        
        return new_copy
    
    def tick(self, dt: float, camera_pos: Pair):
        super().tick(dt, camera_pos)

        self.update_sprite_positions(camera_pos)

        self.update_current_sprite()

    def update_sprite_positions(self, camera_pos: Pair):
        self.sprites.idle_right.x = self.global_pos.first - (
            camera_pos.first - (self.window.width / 2)
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
        
        if self.sprites.attack_right:
            self.sprites.attack_right.x = self.sprites.idle_right.x
            self.sprites.attack_right.y = self.sprites.idle_right.y
        
        if self.sprites.attack_left:
            self.sprites.attack_left.x = self.sprites.idle_right.x - self.attack.range
            self.sprites.attack_left.y = self.sprites.idle_right.y
        
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

    def spawn(self, pos: Pair, direction):
        self.global_pos = pos.copy()
        if direction == Direction.LEFT:
            self.velocity.first *= -1
        self.sprites.SetVisible(self.sprites.idle_right)
        self.spawn_pos = pos

    def isExpired(self):
        if not self.spawn_pos:
            return False
        
        dist = distance(self.spawn_pos, self.global_pos)
        if dist >= self.range:
            return True
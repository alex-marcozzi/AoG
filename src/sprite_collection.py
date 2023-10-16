import pyglet
from src.helpers.utils import make_sprite, copy_sprite

class SpriteCollection():
    def __init__(self,
                 # ****** need directional sprites
                 idle_right: pyglet.sprite.Sprite,
                 idle_left: pyglet.sprite.Sprite = None,
                 slow_move_right: pyglet.sprite.Sprite = None,
                 slow_move_left: pyglet.sprite.Sprite = None,
                 fast_move_right: pyglet.sprite.Sprite = None,
                 fast_move_left: pyglet.sprite.Sprite = None,
                 attack_right: pyglet.sprite.Sprite = None,
                 attack_left: pyglet.sprite.Sprite = None,
                 damaged_right: pyglet.sprite.Sprite = None,
                 damaged_left: pyglet.sprite.Sprite = None,
                 ) -> None:
        self.idle_right = idle_right
        self.idle_left = idle_left
        self.slow_move_right = slow_move_right
        self.slow_move_left = slow_move_left
        self.fast_move_right = fast_move_right
        self.fast_move_left = fast_move_left
        self.attack_right = attack_right
        self.attack_left = attack_left
        self.damaged_right = damaged_right
        self.damaged_left = damaged_left

        self.current = self.idle_right
    
    def copy(self):
        new_copy = SpriteCollection(idle_right=copy_sprite(self.idle_right),
                                    idle_left=copy_sprite(self.idle_left) if self.idle_left else None,
                                    slow_move_right=copy_sprite(self.slow_move_right) if self.slow_move_right else None,
                                    slow_move_left=copy_sprite(self.slow_move_left) if self.slow_move_left else None,
                                    fast_move_right=copy_sprite(self.fast_move_right) if self.fast_move_right else None,
                                    fast_move_left=copy_sprite(self.fast_move_left) if self.fast_move_left else None,
                                    attack_right=copy_sprite(self.attack_right) if self.attack_right else None,
                                    attack_left=copy_sprite(self.attack_left) if self.attack_left else None,
                                    damaged_right=copy_sprite(self.damaged_right) if self.damaged_right else None,
                                    damaged_left=copy_sprite(self.damaged_left) if self.damaged_left else None)
        return new_copy

    def SetVisible(self, sprite: pyglet.sprite.Sprite):
        self.current.visible=False
        sprite.visible=True
        self.current = sprite
        # if sprite_type.lower() == "idle":
        #     self.idle_right.visible = True
        #     if self.slow_move: self.slow_move.visible = False
        #     if self.fast_move: self.fast_move.visible = False
        #     if self.attack: self.attack.visible = False
        #     if self.damaged: self.damaged.visible = False
        # elif sprite_type.lower() == "slow_move":
        #     self.idle_right.visible = False
        #     if self.slow_move: self.slow_move.visible = True
        #     if self.fast_move: self.fast_move.visible = False
        #     if self.attack: self.attack.visible = False
        #     if self.damaged: self.damaged.visible = False
        # elif sprite_type.lower() == "fast_move":
        #     self.idle_right.visible = False
        #     if self.slow_move: self.slow_move.visible = False
        #     if self.fast_move: self.fast_move.visible = True
        #     if self.attack: self.attack.visible = False
        #     if self.damaged: self.damaged.visible = False
        # elif sprite_type.lower() == "attack":
        #     self.idle_right.visible = False
        #     if self.slow_move: self.slow_move.visible = False
        #     if self.fast_move: self.fast_move.visible = False
        #     if self.attack: self.attack.visible = True
        #     if self.damaged: self.damaged.visible = False
        # elif sprite_type.lower() == "damaged":
        #     self.idle_right.visible = False
        #     if self.slow_move: self.slow_move.visible = False
        #     if self.fast_move: self.fast_move.visible = False
        #     if self.attack: self.attack.visible = False
        #     if self.damaged: self.damaged.visible = True
        # else:
        #     raise Exception(f"Exception: invalid sprite type: {sprite_type}.")

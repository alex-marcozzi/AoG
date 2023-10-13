import pyglet
from src.helpers.utils import make_sprite, copy_sprite

class SpriteCollection():
    def __init__(self,
                 # ****** need directional sprites
                 idle: pyglet.sprite.Sprite,
                 slow_move: pyglet.sprite.Sprite = None,
                 fast_move: pyglet.sprite.Sprite = None,
                 attack: pyglet.sprite.Sprite = None,
                 damaged: pyglet.sprite.Sprite = None
                 ) -> None:
        self.idle = idle
        self.slow_move = slow_move
        self.fast_move = fast_move
        self.attack = attack
        self.damaged = damaged
    
    def copy(self):
        new_copy = SpriteCollection(idle=copy_sprite(self.idle),
                                    slow_move=copy_sprite(self.slow_move) if self.slow_move else None,
                                    fast_move=copy_sprite(self.fast_move) if self.fast_move else None,
                                    attack=copy_sprite(self.attack) if self.attack else None,
                                    damaged=copy_sprite(self.damaged) if self.damaged else None)
        return new_copy

    def SetVisible(self, sprite_type: str):
        if sprite_type.lower() == "idle":
            self.idle.visible = True
            if self.slow_move: self.slow_move.visible = False
            if self.fast_move: self.fast_move.visible = False
            if self.attack: self.attack.visible = False
            if self.damaged: self.damaged.visible = False
        elif sprite_type.lower() == "slow_move":
            self.idle.visible = False
            if self.slow_move: self.slow_move.visible = True
            if self.fast_move: self.fast_move.visible = False
            if self.attack: self.attack.visible = False
            if self.damaged: self.damaged.visible = False
        elif sprite_type.lower() == "fast_move":
            self.idle.visible = False
            if self.slow_move: self.slow_move.visible = False
            if self.fast_move: self.fast_move.visible = True
            if self.attack: self.attack.visible = False
            if self.damaged: self.damaged.visible = False
        elif sprite_type.lower() == "attack":
            self.idle.visible = False
            if self.slow_move: self.slow_move.visible = False
            if self.fast_move: self.fast_move.visible = False
            if self.attack: self.attack.visible = True
            if self.damaged: self.damaged.visible = False
        elif sprite_type.lower() == "damaged":
            self.idle.visible = False
            if self.slow_move: self.slow_move.visible = False
            if self.fast_move: self.fast_move.visible = False
            if self.attack: self.attack.visible = False
            if self.damaged: self.damaged.visible = True
        else:
            raise Exception(f"Exception: invalid sprite type: {sprite_type}.")

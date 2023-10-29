import pyglet
from src.helpers.utils import std_speed, block_width, make_sprite
from src.helpers.interfaces import Pair
from src.entity_classes.pickup import Pickup
from src.sprite_collection import SpriteCollection
from src.helpers.globals import Direction

class WizardPickup(Pickup):
    def __init__(
        self,
        window,
        global_pos: Pair,
        batch,
    ):
        sprites = SpriteCollection(idle_right=make_sprite(sprite_filename="assets/images/wizard_pickup.png",
                                                    width=block_width(window) / 2,
                                                    height=block_width(window) / 2,
                                                    visible=True,
                                                    batch=batch),
                                    idle_left=make_sprite(sprite_filename="assets/images/wizard_pickup.png",
                                                    width=block_width(window) / 2,
                                                    height=block_width(window) / 2,
                                                    visible=False,
                                                    batch=batch),)
        
        super().__init__(
            window,
            sprites,
            global_pos,
            block_width(window) / 2,
            block_width(window) / 2,
            batch,
        )
        self.direction = Direction.RIGHT
        # self.modifires = ["dangerous"]

    def copy(self):
        new_copy = WizardPickup(window=self.window,
                             global_pos=self.global_pos,
                             batch=self.batch)
        
        return new_copy
    




####################################################################################################################
# TODO:
#       1. 
#
#
#
# IDEAS:
#       1. charge attack for Wizard powerup: can charge for like 10 seconds to shoot a massive projectile, but lost powerup after
#
#
#
####################################################################################################################

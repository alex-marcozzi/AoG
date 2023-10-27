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
            block_width(window),
            block_width(window),
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
#       1. add different player classes for powerups (have default one, one that can hit, one that can shoot, etc.)
#       2. make it so player can pick up powerups
####################################################################################################################

import pyglet
from src.helpers.utils import std_speed, block_width, make_sprite
from src.helpers.interfaces import Pair
from src.helpers.context import Context
from src.entity_classes.pickup import Pickup
from src.sprite_collection import SpriteCollection
from src.helpers.globals import Direction

class WizardPickup(Pickup):
    def __init__(
        self,
        context: Context,
        global_pos: Pair,
    ):
        sprites = SpriteCollection(idle_right=make_sprite(sprite_filename="assets/images/wizard_pickup.png",
                                                    width=context.block_w / 2,
                                                    height=context.block_w / 2,
                                                    visible=True,
                                                    batch=context.batch),
                                    idle_left=make_sprite(sprite_filename="assets/images/wizard_pickup.png",
                                                    width=context.block_w / 2,
                                                    height=context.block_w / 2,
                                                    visible=False,
                                                    batch=context.batch),)
        
        super().__init__(
            context,
            sprites,
            global_pos,
            context.block_w / 2,
            context.block_w / 2,
        )
        self.direction = Direction.RIGHT
        # self.modifires = ["dangerous"]

    def copy(self):
        new_copy = WizardPickup(context=self.context,
                             global_pos=self.global_pos,)
        
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

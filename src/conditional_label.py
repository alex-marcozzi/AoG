import pyglet
from src.helpers.interfaces import Pair
from src.helpers.context import Context
from src.entity import Entity

class ConditionalLabel:
    def __init__(self, context: Context, text: str = None, sprite: pyglet.sprite.Sprite = None):
        self.context = context
        if text:
            self.label = pyglet.text.Label(
                text,
                font_name="Times New Roman",
                font_size=24,
                x=0,
                y=0,
                z=1, # figure out how to get this to not show up infront of popup
                anchor_x="center",
                anchor_y="center",
                batch=context.batch,
            )
        elif sprite:
            self.label = sprite
            sprite.x = 0
            sprite.y = 0

        self.label.visible = False
    
    def update(self, entity: Entity = None):
        if not entity:
            self.label.visible = False
        else:
            self.label.visible = True
            self.label.x = entity.sprites.current.x + (entity.sprites.current.width / 2)
            self.label.y = entity.sprites.current.y + entity.sprites.current.height + (self.context.block_w / 2)
import os
import pyglet
from src.engine import Engine
from src.entity import Entity

window = pyglet.window.Window(fullscreen=False)
# window.set_vsync(True)
fpsdisplay = pyglet.window.FPSDisplay(window=window)

engine = Engine(window)


@window.event
def on_key_press(symbol, modifiers):
    engine.handle_key_press(symbol, modifiers)


@window.event
def on_key_release(symbol, modifiers):
    engine.handle_key_release(symbol, modifiers)


@window.event
def on_draw():
    # engine.tick()
    window.clear()
    engine.draw()
    fpsdisplay.draw()

def update(dt: float):
    engine.tick(dt)

pyglet.clock.schedule_interval(update, 1/30.0)
pyglet.app.run()

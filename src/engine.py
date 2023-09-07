import pyglet

class Engine:
    def __init__(self, window):
        self.screen_mapping = {
            "STARTUP": "startup_screen_class_goes_here",
            "TITLE": "title_screen_class_goes_here",
            "PAUSE": "pause_screen_class_goes_here",
            "GAME": "game_screen_class_goes_here",
        }

        self.current_screen = ""
        self.window = window
        self.label = "engine test"
    
    def tick(self):
        #self.screen_mapping[self.current_screen].tick()
        self.label = self.label
        pass

    def draw(self):
        #self.screen_mapping[self.current_screen].draw()
        pyglet.text.Label(self.label,
                          font_name='Times New Roman',
                          font_size=36,
                          x=self.window.width//2, y=self.window.height//2,
                          anchor_x='center', anchor_y='center').draw()

    def handle_key_press(self, symbol, modifiers):
        #pass input to screens
        self.label = self.label + "1"
        pass

    def handle_key_release(self, symbol, modifiers):
        #pass input to screens
        pass

import pyglet
from src.helpers.context import Context
from src.popup import Popup
from src.dialogue import Dialogue

class DialoguePopup(Popup):
    def __init__(self, context: Context, dialogue: Dialogue):
        super().__init__(context=context,
                         background_sprite_filename="assets/images/orange.png",
                         percent_width=0.75,
                         percent_height=0.75)

        self.root: Dialogue = dialogue
        self.current: Dialogue = self.root

        self.options = []
        self.labels = []
        self.top_label = None

        self.get_options()
        self.get_labels()
        
    def get_options(self):
        self.options = []
        for key in self.current.children:
            print(key)
            self.options.append(key)
    
    def choose_option(self, text):
        if text in self.current.children:
            self.current = self.current.children[text]
        self.get_options()
        self.get_labels()
        self.activate()

    def get_labels(self):
        for label in self.labels:
            label.visible = False

        if self.top_label:
            self.top_label.visible = False
        self.top_label = pyglet.text.Label(
                self.current.text,
                font_name="Times New Roman",
                font_size=24,
                x=self.background_sprite.x + (self.background_sprite.width / 2),
                y=self.background_sprite.y + self.background_sprite.height - (self.background_sprite.height / 10),
                z=3,
                anchor_x="center",
                anchor_y="center",
                batch=self.context.batch,
            )

        self.top_label.visible = False

        counter = 1
        self.labels: list[pyglet.text.Label] = []
        for option in self.options:
            label = pyglet.text.Label(
                f"{counter}. {option}",
                font_name="Times New Roman",
                font_size=24,
                x=self.background_sprite.x + (self.background_sprite.width / 5),
                y=self.background_sprite.y + (self.background_sprite.height - (counter * (self.background_sprite.height * (1 / (len(self.options) + 1))))),
                z=10,
                anchor_x="left",
                anchor_y="center",
                batch=self.context.batch,
            )
            label.visible = False
            counter += 1

            self.labels.append(label)
        
    def activate(self):
        super().activate()
        for label in self.labels:
            label.visible = True
        
        if self.top_label:
            self.top_label.visible = True
        # self.background_sprite.visible = False

        # self.get_options()
        # self.get_labels()
    
    def deactivate(self):
        super().deactivate()

        for label in self.labels:
            label.visible = False
        
        if self.top_label:
            self.top_label.visible = False
    
    def handle_key_press(self, key):
        print("IN HERE")
        if key == pyglet.window.key._1:
            if len(self.options) >= 1:
                self.choose_option(self.options[0])
        elif key == pyglet.window.key._2:
            if len(self.options) >= 2:
                self.choose_option(self.options[1])
        elif key == pyglet.window.key._3:
            if len(self.options) >= 3:
                self.choose_option(self.options[2])
        elif key == pyglet.window.key._4:
            if len(self.options) >= 4:
                self.choose_option(self.options[3])
import pyglet

class Dialogue:
    def __init__(self, text: str):
        self.text = text
        self.children: dict[str, Dialogue] = {}

    def add_response(self, response_text: str, child_dialogue: "Dialogue" = None):
        self.children[response_text] = child_dialogue

        return child_dialogue
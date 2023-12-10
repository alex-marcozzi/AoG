import pyglet
from src.dialogue import Dialogue

# conversation tree, where each node is a Dialogue object
class Conversation:
    def __init__(self):
        self.root = Dialogue("Hi goose!")

        hello1 = self.root.add_response(response_text="Hello.", child_dialogue=Dialogue("How are you?"))
        great2 = hello1.add_response(response_text="Great!", child_dialogue=Dialogue("Awesome!"))
        ok2 = hello1.add_response(response_text="Eh, I'm ok.", child_dialogue=Dialogue("Something wrong?"))
        no3 = ok2.add_response(response_text="No, I'm alright.", child_dialogue=Dialogue("Ok, see you around!"))
        yes3 = ok2.add_response(response_text="Yeah, I'm out of weed :/.", child_dialogue=Dialogue("Oh no."))
        kys1 = self.root.add_response(response_text="Kys!", child_dialogue=Dialogue("Rude :("))

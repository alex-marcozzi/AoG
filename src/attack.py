import pyglet
import time
from src.entity_classes.projectile import Projectile


class Attack:
    def __init__(
        self,
        range: float,
        duration: float,
        damage: int,
        cooldown: int,
        projectiles: list[Projectile] = None,
    ):
        # self.hitboxes = hitboxes
        self.range = range
        self.duration = duration
        self.damage = damage
        self.cooldown = cooldown
        self.projectiles = projectiles

        self.thrown_time = None
        self.has_fired_projectiles = False

    def Throw(self):
        # if attack already in progress, we have to wait until it's finished to throw again
        if self.inProgress():
            return

        self.thrown_time = time.time()
        self.has_fired_projectiles = False

    def inProgress(self):
        now = time.time()
        if self.thrown_time and now <= self.thrown_time + self.duration:
            return True
        
        return False
    
    def isUsable(self):
        if not self.thrown_time:
            return True

        now = time.time()
        return now > self.thrown_time + self.duration + self.cooldown

    # def Hit(self, character: Character):
    #     # when we add modifiers later we could do checking here:
    #     # if "poisonous" in self.modifiers:
    #     #       etc.

    #     character.takeDamage(amount=self.damage)
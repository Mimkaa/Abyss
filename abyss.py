import pygame as pg
from colorful_fluid import *
from outline import *
from agent import *
vec = pg.Vector2


class Abyss:
    def __init__(self, game):
        self.game = game
        self.outline = Outline(100, 400, 30, (300, 200), 30)
        self.fluid = Fluid(28, 0.00001, 640)
        self.angle = 0
        self.agent1 = Agent(self.fluid, (5, 5), (1, 1), math.pi/4, BLUE, 0.4)
        self.agent2 = Agent(self.fluid, (7, 3), (1, 1), math.pi/4, RED, 0.4)
        self.agent3 = Agent(self.fluid, (3, 7), (1, 1), math.pi/4, GREEN, 0.4)

        self.outline_image = pg.Surface((HEIGHT, HEIGHT))
        self.fluid_image = pg.Surface((HEIGHT, HEIGHT))

    def update(self):
        # update portion of the game loop
        self.outline.update(self.game.dt)
        params = (20, 1)
        self.agent1.update(params[0], params[1], self.game.dt)
        self.agent2.update(params[0], params[1], self.game.dt)
        self.agent3.update(params[0], params[1], self.game.dt)


        self.fluid.update(self.game.dt)

    def draw(self, surf):
        self.outline.draw(self.outline_image)
        self.fluid.draw(self.fluid_image)
        self.outline_image.blit(self.fluid_image,(0,0),None,pg.BLEND_RGBA_MULT)
        surf.blit(self.outline_image,(0, 0))
        # self.agent1.draw(surf, 100)
        # self.agent2.draw(surf, 100)
        # self.agent3.draw(surf, 100)
from p5 import *
#class for Boid, has x and y coords for position and width and height of the object
class Boid():

    def __init__(self, x, y, width, height):
        self.position = Vector(x, y)


    def show(self):
        stroke(255)
        circle((self.position.x, self.position.y), 10)
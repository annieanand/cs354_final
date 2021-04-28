from p5 import *
import numpy as np
from boids import Boid

width = 1000
height = 1000
flock = []
#create the flock (random points) - 10 
for i in range(0,10):
    flock.append(Boid(np.random.rand()*1000, np.random.rand()*1000,width, height))
#sets up canvas to run once with above width and height
def setup():
    size(width, height) 

#draw the background
def draw():
    is_pressed = False
    background(30, 30, 47)
    if mouse_is_pressed:
        is_pressed = True
    #loop through the flock array to show the boid
    for b in flock:
        b.bounding()
        b.show()
        b.apply_behavior(flock)
        b.update(is_pressed)    


if __name__ == '__main__':
    run()

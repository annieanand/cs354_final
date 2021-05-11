from p5 import *
import numpy as np
from boids import Boid
 
width = 1000
height = 800
flock = []

#create the flock (random points) - 10 
for i in range(0,15):
    flock.append(Boid(np.random.rand()*1000, np.random.rand()*1000,width, height))

#sets up canvas to run once with above width and height
def setup():
    size(width, height) 

#draw the background
def draw():
    m_is_pressed = False
    k_is_pressed = False
    background(30, 30, 47)
    line((500,0), (500,800))#create the obstacle as a line from midway through width with a length up and down on the window
    if mouse_is_pressed:
        m_is_pressed = True
    if key_is_pressed:
        if str(key) == "a":
           flock.append(Boid(np.random.rand()*1000, np.random.rand()*1000,width, height)) 
           k_is_pressed = True
    #loop through the flock array to show the boid
    for b in flock:
        b.bounding()
        b.show()
        b.apply_behavior(flock)
        b.update(m_is_pressed)    


if __name__ == '__main__':
    run()

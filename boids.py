from p5 import *
#class for Boid, has x and y coords for position and width and height of the object
#define position, velocity, and accelerations
class Boid():

    def __init__(self, x, y, width, height):
        self.position = Vector(x, y)
        v = ((np.random.rand()-0.5)*10, (np.random.rand()-0.5)*10) #range between -5 and 5
        self.velocity = Vector(*v) #vector is built in
        v =  ((np.random.rand() - 0.5)/2, (np.random.rand() - 0.5)/2) #btwn -.25 and .25
        self.acceleration = Vector(*v) 

        self.width = width
        self.height = height
        self.max_speed = 7
  
    def show(self):
        stroke(255)
        circle((self.position.x, self.position.y), 10) #change later?
  
    def update(self, is_pressed):
        if is_pressed == True:
            return
        self.position = self.position + self.velocity #update position by adding the direction vector
        self.velocity = self.velocity + self.acceleration

        #create a max speed so that the boids continue with smoother movements
        if np.linalg.norm(self.velocity) > self.max_speed:
            #normalize vectors
            self.velocity = self.velocity / np.linalg.norm(self.velocity) * self.max_speed
        self.acceleration = Vector(np.zeros(1), np.zeros(1))
    #create boundaries for boids
    def bounding(self):
        if self.position.x > self.width:
            self.position.x = 0 
        elif self.position.x < 0: 
            self.position.x = self.width
        
        if self.position.y > self.height:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = self.height


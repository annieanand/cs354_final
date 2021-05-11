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
        self.max_see_ahead = 2
        self.max_avoid_force = 5
        self.width = width
        self.height = height
        self.max_speed = 10
        self.max_force = 1
        self.distance_to_next = 200
       
        self.avoidance_force = self.position + (self.velocity/np.linalg.norm(self.velocity)) * self.max_see_ahead

    def show(self):
        stroke(255)
        circle((self.position.x, self.position.y), 5) #circle with a radius of 5
        
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
        if self.position.x >= self.width: #checks if the x position is greater than width
            self.position.x = self.width-50 #resets position to move left and changes velocity to be faster and go the opp way
            self.velocity *= -5
            
        elif self.position.x <= 0: #checks if x position is less than 0
            
            self.position.x = 50
            self.velocity*= -5
        if self.position.y >= self.height: #checks if y position is above height
            
            self.position.y = self.height-50
            self.velocity *= -5
        elif self.position.y <= 0: #checks if y position is below 0
            
            self.position.y = 50
            self.velocity *= -5
         
   
    #now to add behavior to the flock
    #steering = avg_vec of boids - self.velocity 
    #helps with velocity matching

    def align(self, boids):
        steer = Vector(np.zeros(1), np.zeros(1)) #initialize steering vector
        total = 0  
        avg_dir = Vector(np.zeros(1), np.zeros(1)) #average dir of boids
        for b in boids: # loop through the boids
            if np.linalg.norm(b.position - self.position) < self.distance_to_next: #check which boids are within appropriate distance
                avg_dir += b.velocity #if it is then add the boid velocity to the avg direction
                total = total + 1 # to see how many boids are near
            
        if total > 0:
            avg_dir = avg_dir / total #find the new average 
            avg_dir = Vector(*avg_dir) #create new vec with value
            avg_dir = (avg_dir / np.linalg.norm(avg_dir)*self.max_speed) #normalize it for direction and multiply by speed
            steer = avg_dir - self.velocity  #calculate the steering direction now
        return steer 
    
    #add in cohesion next - steer toward center of mass
    #assume boids are all the same mass! 
    def cohesion(self,boids):
        steer = Vector(np.zeros(1), np.zeros(1)) #initialize steering vector
        total = 0
        com = Vector(np.zeros(1), np.zeros(1)) #initialize center of mass
        for b in boids:
            if np.linalg.norm(b.position - self.position) > self.distance_to_next:
                com += b.position #change center of mass based on boid position with respect to neighbors
                total += 1
        if total >0:
            com = com /total #set center of mass to the average of the boids
            com = Vector(*com)
            com_to_boid = com - self.position
            if np.linalg.norm(com_to_boid) > 0: # check if the boid is not the com
                com_to_boid = (com_to_boid / np.linalg.norm(com_to_boid)) * self.max_speed #normalize vector towards com
            steer = com_to_boid - self.velocity
            if np.linalg.norm(steer) > self.max_force: #controls for the magnitude for steering
                steer = (steer / np.linalg.norm(steer)) * self.max_force #normalize!
        return steer
    
    #last step, separation
    #avoid getting too close to others
    def separation(self,boids):
        steer = Vector(np.zeros(1), np.zeros(1))
        total = 0
        avg_dir = Vector(np.zeros(1), np.zeros(1))
        for b in boids: #loop through boids
            dist = np.linalg.norm(b.position - self.position) #normalize vector between next boid (direction of escape)
            if self.position != b.position and dist < self.distance_to_next: #check whether the current boid is the same as the next position, and if it is within appropriate radius
                distance_away = self.position - b.position #calculate distance away 
                distance_away = distance_away/dist #change the distance - based on the direcction of escape                
                avg_dir += distance_away #append to avg direction vec
                total = total +1
            if total > 0:
                avg_dir = avg_dir / total #set new average direction
                avg_dir = Vector(*avg_dir)
                if np.linalg.norm(steer) > 0: #check if the steer dir is positive
                    avg_dir = (avg_dir / np.linalg.norm(steer)) *self.max_speed  #normalize it and mult by speed
                steer = avg_dir - self.velocity #adjust the steer vector again
                if np.linalg.norm(steer) > self.max_force: #check if the steer magnitude is over the max force. if it is:
                    steer = (steer / np.linalg.norm(steer)) *self.max_force #weight the steer by force (based on dist away)
        return steer

    #avoid running into boundaries 
    def line_collision_detect(self,boids):
        

        #the ahead vector represents the perception of the boid "ahead"
        ahead = self.position + self.velocity * self.max_see_ahead
        criteria = False
        
        if abs(ahead.x - self.width/2) < 20: # set threshold to 20 ; checks whether it is about 20 away from the middle line
        

            self.avoidance_force =  self.avoidance_force  + (ahead - Vector(self.width/2, ahead.y)) # avoidance force is added to the difference btwn ahead and the obstacle x val
            self.avoidance_force = (self.avoidance_force/np.linalg.norm(self.avoidance_force)) * self.max_avoid_force #normalize
            self.velocity = self.velocity + self.avoidance_force
            self.position = self.position + self.velocity
            criteria = True
        
        if (ahead.x) <= 50:
            self.avoidance_force = self.avoidance_force  + (ahead - Vector(0.0, ahead.y))
            self.avoidance_force = (self.avoidance_force/np.linalg.norm(self.avoidance_force)) * self.max_avoid_force 

            self.velocity = self.velocity + self.avoidance_force
            self.position = self.position + self.velocity
            criteria = True
 

       
        if (ahead.x) >= self.width -50:
            self.avoidance_force = self.avoidance_force  + (ahead - Vector(self.width -30, ahead.y))
            self.avoidance_force = (self.avoidance_force/np.linalg.norm(self.avoidance_force)) * self.max_avoid_force 

            self.velocity = self.velocity + self.avoidance_force
            self.position = self.position + self.velocity   
            criteria = True
           
        if (ahead.y <= 50):
            self.avoidance_force = self.avoidance_force  + (ahead - Vector(ahead.x,0.0))
            self.avoidance_force = (self.avoidance_force/np.linalg.norm(self.avoidance_force)) * self.max_avoid_force 

            self.velocity = self.velocity + self.avoidance_force
            self.position = self.position + self.velocity 
            criteria = True
        if (ahead.y >= self.height-50):
            self.avoidance_force = self.avoidance_force  + (ahead - Vector(ahead.x, self.height-30))
            self.avoidance_force = (self.avoidance_force/np.linalg.norm(self.avoidance_force)) * self.max_avoid_force 
            self.velocity = self.velocity + self.avoidance_force
            self.position = self.position + self.velocity 
            criteria = True
        
        if criteria:
            return self.avoidance_force
        else:
            return Vector(0.0,0.0)
        
    
    #function to apply the different behaviors on the boids
    def apply_behavior(self, boids):
        aligned = self.align(boids)
        self.acceleration += aligned *0.25

        cohe =  self.cohesion(boids)
        self.acceleration += cohe * 0.75

        separation = self.separation(boids)
        self.acceleration += separation * 0.75

        #apply the avoidance
        avoidance = self.line_collision_detect(boids)
        self.acceleration += avoidance*.75
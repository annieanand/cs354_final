# cs354_final
CS354/BME345 Final Project Report (Flocking Simulation Model)


Necessary Libraries: p5, numpy, glfw
Built on: Python 3.9.1

The premise of this project is to create a flocking simulation model that utilizes the behaviors primarily outlined in Craig Reynolds’ “Flocks, Herds, and Schools: A Distributed Behavioral Model”. The main motivation behind this simulation is to be able to visualize the navigation of a particular “bird” or what we call a boid in this simulation, based on a variety of behaviors relative to objects nearby. A flock is defined as a group of discrete boids that have individual properties but have overall motion that seems fluid. In fact, the aggregate result is based on the individual entities and their local perception. The model used must support the following behaviors: collision avoidance, velocity matching, and flock centering. These behaviors ensure that flockmates avoid collisions with each other, roughly match the velocity of neighbors, and stay close (but not too close)! An additional behavior that I have added into this project is obstacle avoidance based on a pre-set field of perception. If an object “senses” that it is approaching an obstacle (i.e. the boundary or line appears in its perception straight ahead), an avoidance forces is added on. Each of these behaviors provide a suggestion on which way to steer the boid. The acceleration is normalized and the total among behaviors is averaged (usually with weights). 
For this project, I decided to primarily focus on recreating a flocking simulation with the behaviors mentioned above. Below you will see the general code structure for this project. As seen here, the main sets up the boids, and creates the GUI to display the simulation. There is also a boid class which consists of methods for the different behaviors described above.
 

Below are some code snippets from the major sections. 

Here is the code within the main. As can be seen here, the libraries used are numpy and p5 (to help with visualization). Then, the boids are created as random points in the canvas window and appended to a flock list. There are additionally two functions: setup() and draw(). Setup() creates the canvas and draw controls() any elements on the canvas and any potential user input. The user inputs here include pressing and holding the left click on a mouse to pause the movement, and hitting the key ‘a’ will add another boid to the flock. The default is 15.
 
 
Then, in the Boid class there were multiple behaviors implemented. It starts of by initializing some attributes of the boids including their position, velocity, and acceleration. It also has a few other parameters such as max_avoid_force (used to limit the avoidance force), max_see_ahead (used for perception from boids), and max_speed (used to limit the velocity), distance_to_next (used as a parameter within separation). Avoidance force is also initialized here.
 

Next, here are some of the functions within the class. The show() function essentially just creates the boids as circles with a given radius and color. The update() function first checks if one of the user input criteria is met (if the mouse is held down) in which case it doesn’t update position/velocity. Otherwise, it updates it every time while checking if it has hit the maximum speed yet and normalizing the velocity accordingly.
 
Next is the bounding function which basically prevents boids from exiting the boundaries of the windows we have created. If it hits any of the boundaries, it is meant to adjust its position and go in the opposite direction at a slightly faster speed. 
 

Now we finally start implementing some of the behaviors. The first one is alignment, which is essentially velocity matching of nearby flockmates. It loops through the boids to see which ones are within an appropriate pre-set distance to the next one, and those are the ones that this behavior applies to. If so, it adds that particular boid’s velocity to the overall average, and increments a counter. Then, it checks if there were more than one to find the new average and creates a normalized vector from it. Finally, the steering direction for that particular boid can be calculated based on the difference from the average velocity.

 
The next behavior implemented is cohesion, which creates a steer towards the center of mass of the flock. In this project,  I assumed all the boids were the same mass, but that could be easily altered in the future. The boids are looped through again and the center of mass essentially adds the positions of all the boids and divides by the total to find the average. Then, the individual center of masses relative to the boids can be found by subtracting its position from the average center of mass. If the boid is not the center of mass itself, the normalized vector is created and added into the steer component. There is also a max_force parameter initialized earlier that controls the magnitude for the steering and is incorporated here as well.
 

Next, is the separation behavior. This behavior helps boids avoid getting too close to each other when in the flock. The boids are looped through, and the distance between all of the other boids and the current one are found. Then, we check whether the current boid’s position is not the same as the others and if the distance is within the threshold. If so, the distance away value is added to the average direction. Then, the new average direction is normalized and the steer angle is adjusted based on max_speed and max_force, similar to in cohesion().
 
Finally, there is a function for avoidance with obstacles called line_collision_detect(). This uses the ahead vector which is basically just how far ahead that the boids can “see” based on a max_see_ahead vector. There are a few if conditions that basically check whether the boids are a certain distance away from the obstacles (which have been set to the different boundaries as ewll as the middle line on the canvas).  Some of those conditions are shown in the code snippet below. The avoidance force is then calculated based on the original value which is set to: self.position + (self.velocity/np.linalg.norm(self.velocity)) * self.max_see_ahead, by adding the difference between the perception ahead vector minus the obstacle. It is then normalized.
 
Finally, there is a function to apply all of these behaviors by adding them to the overall acceleration request. The behaviors weights were all tuned as the simulation was tested. As can be seen below, the cohesion, separation, and avoidance were all weighted somewhat more heavily than alignment in order to ensure that they are generally flocking and avoiding obstacles, and velocity matching is not as much of a priority.
 

Because of the nature of this project, it is hard to show artifacts for the simulation since it is easier to be seen when run as the boids are constantly moving. However, below is a screenshot showing the flocking nature of the boids, which also manage to avoid the obstacles on the side and in the middle. Unfortunately, at some points the boids may still have to cross over the middle line, but this is because their other three behaviors overtake the urge to avoid the obstacle.
 



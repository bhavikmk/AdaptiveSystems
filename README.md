# AdaptiveSystems

## 1. Boid Simulation

This project implements a Boid Flocking Simulation using Python and Bokeh for interactive visualization.

The simulation models the flocking behavior of simple agents called boids. Each boid follows three basic rules to mimic the natural movement seen in flocks of birds, schools of fish, or herds of animals:

* Alignment: Steer towards the average heading of local neighbors.
* Cohesion: Move towards the average position (center of mass) of local neighbors.
* Separation: Avoid crowding neighbors by steering away if they get too close.

### How It Works

#### Initialization

* 50 boids are randomly placed within an 800x600 area.
* Each boid is given a random initial velocity.
Simulation Loop:

* For each boid, neighbors within a certain radius are identified.
* The boid's velocity is updated based on the three rules above, each weighted by a user-adjustable parameter.
* Boids wrap around the edges of the simulation area.
Interactivity:

* Three sliders allow real-time adjustment of the weights for alignment, cohesion, and separation.
* The visualization updates every 50 milliseconds.

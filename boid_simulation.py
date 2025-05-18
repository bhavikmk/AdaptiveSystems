from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, Slider
from bokeh.layouts import column, row
import numpy as np

# Simulation parameters
N_BOIDS = 50
WIDTH, HEIGHT = 800, 600
MAX_SPEED = 4.0
NEIGHBOR_RADIUS = 50
AVOID_RADIUS = 20

# Boid rules weight (can be updated via sliders)
alignment_weight = 1.0
cohesion_weight = 1.0
separation_weight = 1.5

# Initialize positions and velocities
positions = np.random.rand(N_BOIDS, 2) * [WIDTH, HEIGHT]
velocities = (np.random.rand(N_BOIDS, 2) - 0.5) * MAX_SPEED

source = ColumnDataSource(data=dict(x=positions[:, 0], y=positions[:, 1]))

# Set up plot
plot = figure(width=WIDTH, height=HEIGHT, title="Boid Intelligence: Flocking Simulation")
plot.scatter(x='x', y='y', size=8, color='navy', source=source)

def update():
    global positions, velocities
    new_positions = np.copy(positions)
    new_velocities = np.copy(velocities)

    for i in range(N_BOIDS):
        pos_i = positions[i]
        vel_i = velocities[i]

        neighbors = []
        for j in range(N_BOIDS):
            if i != j:
                dist = np.linalg.norm(positions[j] - pos_i)
                if dist < NEIGHBOR_RADIUS:
                    neighbors.append(j)

        if neighbors:
            # Alignment
            avg_vel = np.mean(velocities[neighbors], axis=0)
            alignment = (avg_vel - vel_i) * alignment_weight

            # Cohesion
            center_of_mass = np.mean(positions[neighbors], axis=0)
            cohesion = (center_of_mass - pos_i) * cohesion_weight * 0.01

            # Separation
            separation = np.zeros(2)
            for j in neighbors:
                diff = pos_i - positions[j]
                dist = np.linalg.norm(diff)
                if dist < AVOID_RADIUS:
                    separation += diff / (dist + 1e-5)
            separation *= separation_weight * 0.05

            # Update velocity
            vel_i += alignment + cohesion + separation

        # Limit speed
        speed = np.linalg.norm(vel_i)
        if speed > MAX_SPEED:
            vel_i = (vel_i / speed) * MAX_SPEED

        new_velocities[i] = vel_i
        new_positions[i] = (pos_i + vel_i) % [WIDTH, HEIGHT]  # wrap around

    positions = new_positions
    velocities = new_velocities
    source.data = dict(x=positions[:, 0], y=positions[:, 1])

# Sliders for interactivity
align_slider = Slider(start=0.0, end=3.0, value=1.0, step=0.1, title="Alignment")
cohesion_slider = Slider(start=0.0, end=3.0, value=1.0, step=0.1, title="Cohesion")
separation_slider = Slider(start=0.0, end=3.0, value=1.5, step=0.1, title="Separation")

def slider_update(attr, old, new):
    global alignment_weight, cohesion_weight, separation_weight
    alignment_weight = align_slider.value
    cohesion_weight = cohesion_slider.value
    separation_weight = separation_slider.value

for slider in [align_slider, cohesion_slider, separation_slider]:
    slider.on_change("value", slider_update)

# Set up layout and document
layout = column(plot, row(align_slider, cohesion_slider, separation_slider))
curdoc().add_root(layout)
curdoc().add_periodic_callback(update, 50)  # milliseconds

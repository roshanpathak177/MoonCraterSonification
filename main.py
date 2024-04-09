import csv
from time import time
import moderngl
from renderer import render, render_moon
from scene import Moon
from shaders import load_shaders
from utils import render_impact_effect

ctx = moderngl.create_context() 
# Load shaders
program = load_shaders(ctx, 'shaders/vertex_shader.glsl', 'shaders/fragment_shader.glsl')

# Create the Moon object
moon = Moon()


# Load the asteroid impact data from the CSV file
asteroid_impacts = []
with open('lunarCraterAges.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header row
    for row in reader:
        time_of_impact, latitude, longitude, diameter = row
        asteroid_impacts.append({
            'time_of_impact': float(time_of_impact),
            'latitude': float(latitude),
            'longitude': float(longitude),
            'diameter': float(diameter),
        })

# Main loop
current_time = 0
previous_time = time.time()
while True:
    current_time = time.time()
    delta_time = current_time - previous_time

    # Update the Moon's rotation
    moon.update(current_time)

    # Render the Moon
    render_moon(program, moon.get_transformation_matrix())

    # Render active asteroid impacts
    for impact in asteroid_impacts:
        if impact.is_active(current_time):
            impact_position = impact.get_impact_position(moon)
            render_impact_effect(program, impact_position, impact.crater_diameter)

    # Update the previous time for the next iteration
    previous_time = current_time
from flask import views
from moderngl import Program
import moderngl
import numpy as np
from pyrr import Matrix44
from time import time

from utils import calculate_impact_position, render_impact_effect

ctx = moderngl.create_context() 

# Load the shaders
with open('vertex_shader.glsl') as f:
    vertex_shader = f.read()

with open('fragment_shader.glsl') as f:
    fragment_shader = f.read()

program = Program(ctx, vertex_shader, fragment_shader)

def creat_moon_vao(ctx, program):
    # Define the Moon's vertex data
    vertices = np.array([
        -1, 1, 0, 0, 1,
        1, 1, 0, 1, 1,
        -1, -1, 0, 0, 0,
        1, -1, 0, 1, 0,
    ])

    # Create the VAO
    vao = ctx.vertex_array(
        program,
        [
            # Map in_vert to the vertices
            (vertices, '3f 2f', ['in_vert', 'in_text']),
        ],
    )

    return vao

# Define the rendering function
def render(ctx, program, vao, time, asteroid_impacts, proj):
    ctx.clear()
    ctx.enable(moderngl.DEPTH_TEST)

    # Set up the view matrix
    view = Matrix44.look_at(
        (10, 5, 10),
        (0, 0, 0),
        (0, 1, 0),
    )

    # Render the asteroid impacts
    for impact in asteroid_impacts:
        # Calculate the impact position on the Moon's surface
        # based on the latitude, longitude, and time of impact
        impact_position = calculate_impact_position(impact)

        # Render the impact effect (e.g., a sphere or particle effect)
        render_impact_effect(impact_position)

    ctx.swap_buffers()

aspect_ratio = 1.0  # Adjust this value to match your window's aspect ratio
proj = Matrix44.perspective_projection(45.0, aspect_ratio, 0.1, 100.0) 

# Render the Moon
def render_moon(program, transformation_matrix):
        
        model = Matrix44.from_y_rotation(time)
        program['model'].write(model.astype('f4').tobytes())
        program['view'].write(views.astype('f4').tobytes())
        program['proj'].write(proj.astype('f4').tobytes())
        vao.render(moderngl.TRIANGLE_STRIP)
        program['model'].write(transformation_matrix.astype('f4').tobytes())
        moon_vao.render(moderngl.TRIANGLE_STRIP)

def render_impact_effect(ctx, program, impact_position, crater_diameter):
    """
    Render the impact effect (e.g., a sphere or particle effect) at the specified `impact_position`.
    """
    # Example: Render a sphere at the impact position with a size based on the crater diameter
    sphere_model = Matrix44.from_translation(impact_position)
    sphere_scale = crater_diameter / 2
    sphere_model = Matrix44.multiply(sphere_model, Matrix44.from_scale([sphere_scale, sphere_scale, sphere_scale]))

    program['model'].write(sphere_model.astype('f4').tobytes())
    sphere_vao.render(moderngl.TRIANGLES)
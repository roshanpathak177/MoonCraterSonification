# utils.py
import moderngl
import numpy as np
from PIL import Image
from pyrr import Vector3, matrix33, Matrix44

from renderer import moon_vao

def load_moon_texture(texture_path):
    """
    Load the Moon texture data from an image file and return it as a numpy array.
    """
    image = Image.open(texture_path)
    image_data = np.array(list(image.getdata()), np.uint8)
    return image_data.reshape(image.size[1], image.size[0], 3)

def calculate_impact_position(impact, moon_radius=1):
    """
    Calculate the position on the Moon's surface where the asteroid should strike,
    based on the latitude, longitude, and time of impact data in the `impact` dictionary.
    """
    lat = impact['latitude'] * np.pi / 180
    lon = impact['longitude'] * np.pi / 180
    time = impact['time_of_impact']

    # Calculate the position on the Moon's surface using spherical coordinates
    x = moon_radius * np.cos(lat) * np.cos(lon)
    y = moon_radius * np.sin(lat)
    z = moon_radius * np.cos(lat) * np.sin(lon)

    # Apply rotation based on time to simulate the Moon's rotation
    rotation_matrix = Matrix44.from_y_rotation(time)
    impact_position = Vector3([x, y, z])
    impact_position = rotation_matrix @ impact_position

    return impact_position

import moderngl
import numpy as np

def create_sphere_vao(ctx, program, resolution=32):
    """
    Create a VAO for a sphere mesh with the specified resolution.
    """
    vertices = []
    indices = []

    # Generate the sphere vertex data
    for y in range(resolution):
        for x in range(resolution):
            theta = np.pi * y / (resolution - 1)
            phi = 2 * np.pi * x / (resolution - 1)

            vertices.extend([
                np.sin(theta) * np.cos(phi),
                np.cos(theta),
                np.sin(theta) * np.sin(phi),
            ])

    # Generate the sphere index data
    for y in range(resolution - 1):
        for x in range(resolution):
            indices.extend([
                y * resolution + x,
                (y + 1) * resolution + x,
                (y + 1) * resolution + (x + 1) % resolution,
                y * resolution + (x + 1) % resolution,
            ])

    vao = ctx.vertex_array(
        program,
        [
            # Map in_vert to the vertices
            (np.array(vertices, dtype='f4'), '3f', 'in_vert'),
        ],
        indices=np.array(indices, dtype='i4'),
    )

    return vao


def render_impact_effect(ctx, program, impact_position, crater_diameter):
    """
    Render the impact effect (e.g., a sphere or particle effect) at the specified `impact_position`.
    """
    # Example: Render a sphere at the impact position with a size based on the crater diameter
    sphere_model = Matrix44.from_translation(impact_position)
    sphere_scale = crater_diameter / 2
    sphere_model = matrix33.multiply(sphere_model, Matrix44.from_scale([sphere_scale, sphere_scale, sphere_scale]))

    program['model'].write(sphere_model.astype('f4').tobytes())
    sphere_vao.render(moderngl.TRIANGLES)

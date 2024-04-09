import moderngl
import numpy as np
from pyrr import Matrix44

# Create an OpenGL context
ctx = moderngl.create_context()

# Load the Moon texture
moon_texture = ctx.texture(size_or_shape=(2048, 1024), components=3, data=load_moon_texture())

# Set up the projection matrix
proj = Matrix44.perspective_projection(45.0, 1.0, 0.1, 1000.0)
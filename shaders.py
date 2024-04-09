# shaders.py
import moderngl

def load_shaders(ctx, vertex_shader_path, fragment_shader_path):
    """
    Load and compile the GLSL shaders from the specified file paths.
    """
    with open(vertex_shader_path) as f:
        vertex_shader = f.read()

    with open(fragment_shader_path) as f:
        fragment_shader = f.read()

    program = moderngl.Program(ctx, vertex_shader, fragment_shader)
    return program
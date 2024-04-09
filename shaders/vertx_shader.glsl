# vertex_shader.glsl
#version 330

uniform mat4 proj;
uniform mat4 view;
uniform mat4 model;

in vec3 in_vert;
in vec2 in_text;

out vec2 v_text;

void main() {
    gl_Position = proj * view * model * vec4(in_vert, 1.0);
    v_text = in_text;
}
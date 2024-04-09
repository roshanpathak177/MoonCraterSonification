# fragment_shader.glsl
#version 330

uniform sampler2D moon_texture;

in vec2 v_text;

out vec4 f_color;

void main() {
    f_color = texture(moon_texture, v_text);
}
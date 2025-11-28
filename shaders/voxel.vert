#version 330 core

layout(location = 0) in vec3 in_pos;      
layout(location = 1) in vec3 in_offset;   
layout(location = 2) in vec2 in_uv;       
layout(location = 3) in vec3 in_normal;
layout(location = 4) in float in_mat_id;

uniform mat4 u_view;
uniform mat4 u_proj;

out vec3 v_normal;
out vec3 v_world_pos;
out vec2 v_uv;
out vec3 v_offset;
out float v_mat_id;


void main() {
    vec3 world_pos = in_pos + in_offset;
    gl_Position = u_proj * u_view * vec4(world_pos, 1.0);

    v_world_pos = world_pos;
    v_normal = in_normal;
    v_uv = in_uv;
    v_offset = in_offset;
    v_mat_id = in_mat_id;
}
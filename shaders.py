VERTEX_SHADER_SRC = """
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

"""

FRAGMENT_SHADER_SRC = """
#version 330 core

in vec3 v_normal;
in vec3 v_world_pos;
in vec2 v_uv;
in vec3 v_offset;

uniform vec3 u_light_pos;
uniform vec3 u_view_pos;

uniform ivec3 u_selected;
uniform bool  u_highlight_selected;

uniform sampler2D u_textures[5];
in float v_mat_id;

out vec4 FragColor;

void main() {
    int mid = int(v_mat_id + 0.5);
    mid = clamp(mid, 0, 4);
    vec3 texColor = texture(u_textures[mid], v_uv).rgb;
    vec3 normal = normalize(v_normal);
    vec3 ambient = 0.6 * texColor;

    vec3 light_dir = normalize(u_light_pos - v_world_pos);
    float diff = max(dot(normal, light_dir), 0.0);
    vec3 diffuse = diff * texColor * 0.75;
    vec3 color = ambient + diffuse;
    
    if (u_highlight_selected) {
        ivec3 voxel = ivec3(round(v_offset));
        if (all(equal(voxel, u_selected))) {
            color = mix(color, vec3(1.0, 0.3, 0.3), 0.6);
        }
    }

    FragColor = vec4(color, 1.0);
}
"""
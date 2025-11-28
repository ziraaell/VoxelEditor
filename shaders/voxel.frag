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
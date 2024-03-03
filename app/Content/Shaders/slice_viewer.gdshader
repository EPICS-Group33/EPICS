shader_type spatial;
render_mode unshaded;
render_mode cull_disabled;
render_mode alpha_to_coverage;


uniform sampler3D texture3D; // Your 3D texture
uniform float slice; // Index of the desired slice (0 to texture_depth - 1)
uniform float alpha_scissor_threshold;
uniform float alpha_antialiasing_edge;
void fragment() {
    // Calculate normalized texture coordinates based on UV and slice index
    vec3 tex_coord = vec3(UV, slice * TIME / 100.0);

    // Sample the desired slice from the 3D texture
    vec4 color = texture(texture3D, tex_coord);

	ALPHA = length(color);

    ALBEDO = color.rgb;

	ALPHA *= length(color);
	ALPHA_SCISSOR_THRESHOLD = alpha_scissor_threshold;
	ALPHA_ANTIALIASING_EDGE = alpha_antialiasing_edge;
}

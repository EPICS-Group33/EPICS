shader_type spatial;
render_mode unshaded, cull_disabled;

uniform sampler3D tex;
uniform float slice = 1.0;

void fragment() {
	vec3 tex_coord = vec3(UV, slice * TIME / 100.0);
	vec4 color = texture(tex, tex_coord);
	ALBEDO = color.rgb;
}
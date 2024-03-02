shader_type spatial;
render_mode unshaded;


uniform float fov = 75.;

group_uniforms NoiseData;
uniform sampler3D noise_tex;
uniform float noise_scale = 1.;
uniform vec3 noise_offset = vec3(0.);
uniform float density_threshold = .5;
uniform float density_multiplier = 1.;

group_uniforms LightData;
uniform vec3 ambient_light = vec3(1.);
uniform float absorption_coef = .000005;
uniform float scattering_coef = .02;

group_uniforms RayMarchData;
uniform int vm_step_count = 100;

group_uniforms BoxData;
uniform vec3 bb_min = vec3(-10.);
uniform vec3 bb_max = vec3(10.);

uniform sampler2D depth_texture : hint_depth_texture;
uniform sampler2D screen_texture : hint_screen_texture;


// For calculating camera direction in world space
vec3 get_camera_direction(vec2 uv, vec2 viewport_size, mat4 inv_view_matrix) {
	// so the original UV is typically in screen space, which is the final space there is.
	// refresher on spaces: object -> world -> camera/view -> clip/ndc -> screen
	// the ray direction is on the world space, so we need to transform this UV into world space.
	// to do that, we first change it to NDC space which normalizes the UV to [-1,1] range
	vec2 normalized_uv = uv * 2. - 1.;
	vec3 dir_ndc = vec3(normalized_uv.x, normalized_uv.y, 1.);

	vec2 resolution = 1. / viewport_size;
	float aspect_ratio = resolution.y / resolution.x;
	float tan_half_fov = tan(radians(fov) * .5);

	// we then construct the camera/view space by taking into account the aspect ratio and FOV.
	vec3 dir_view = normalize(vec3(normalized_uv.x * aspect_ratio * tan_half_fov, normalized_uv.y * tan_half_fov, -1.0));

	// once we do that, we can transform further to world space usingn the inverse view matrix.
	vec4 dir_world = inv_view_matrix * vec4(dir_view, 0.0);

	// return the normalized version of it
	return normalize(dir_world.xyz);
}


vec2 ray_box_intersect(vec3 ro, vec3 rd) {
	vec3 t0 = (bb_min - ro) / rd;
	vec3 t1 = (bb_max - ro) / rd;
	vec3 tmin = min(t0, t1);
	vec3 tmax = max(t0, t1);

	float dst_a = max(max(tmin.x, tmin.y), tmin.z);
	float dst_b = min(tmax.x, min(tmax.y, tmax.z));

	float dst_to_box = max(0., dst_a);
	float dst_through_box = max(0., dst_b - dst_to_box);

	return vec2(dst_to_box, dst_through_box);
}


float get_linear_depth(sampler2D depth_tex, vec2 screen_uv, mat4 inv_pro_mat) {
	float depth = texture(depth_tex, screen_uv).x;
	vec3 ndc = vec3(screen_uv * 2. - 1., depth);
	vec4 view = inv_pro_mat * vec4(ndc, 1.0);
	view.xyz /= view.w;
	return -view.z;
}


float sample_density(vec3 p) {
	vec3 uvw = p * noise_scale * .01 + noise_offset * .01;
	float noise = texture(noise_tex, uvw).x;
	float density = max(0., noise - density_threshold) * density_multiplier;
	return density;
}


vec4 volume_marcher(vec3 ro, vec3 rd, float len, vec3 col) {
	vec3 p = ro;
	float step_size = len / float(vm_step_count - 1);

	float total_density = 0.;

	for (int i = 0; i < vm_step_count; ++i) {
		float cur_density = sample_density(p);
		total_density += cur_density * step_size;
		p += rd * step_size;
	}

	return vec4(col + vec3(total_density), 1.);
}


void vertex() {
	POSITION = vec4(VERTEX, 1.0);
}


void fragment() {
	vec3 original_color = texture(screen_texture, SCREEN_UV).rgb;

	vec3 ro = CAMERA_POSITION_WORLD;
	vec3 rd = get_camera_direction(UV, VIEWPORT_SIZE, INV_VIEW_MATRIX);
	float depth = get_linear_depth(depth_texture, SCREEN_UV, INV_PROJECTION_MATRIX);

	vec2 points = ray_box_intersect(ro, rd);
	float dst_to = points.x;
	float dst_through = min(points.y, depth - dst_to);

	ALBEDO = original_color;

	bool hit = dst_through > 0. && dst_to < depth;
	if (hit) {
		float eps = .001;
		vec3 p = ro + rd * (dst_to + eps);
		vec4 col = volume_marcher(p, rd, dst_through - eps, original_color);
		ALBEDO = col.rgb;
		ALPHA = col.a;
	}
}
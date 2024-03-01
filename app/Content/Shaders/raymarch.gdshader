shader_type spatial;
render_mode unshaded;

varying vec3 position;
varying vec3 camera;

uniform sampler3D inputTexture;

void vertex() {
	position = VERTEX;
}


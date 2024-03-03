extends Node3D
class_name Manager

@onready var slice_mesh = $SliceViewer

var folder_path = "user://slices/"  # Change this to your desired folder path
var texture_name = "combined_texture.res"

func _ready():
	var dir_access = DirAccess.open(folder_path)
	if not dir_access:
		print("Error: Could not open directory:", folder_path)
		return

	var files = dir_access.get_files()
	var image_count = 0

	# Validate all files are PNGs
	for file in files:
		if not file.find(".png", -4):
			print("Warning: Skipping non-PNG file:", file)

	var data = []

	# Get largest image dimension for texture size
	var max_width = 0
	var max_height = 0
	for file in files:
		if file.ends_with(".png"):
			var image = Image.load_from_file(folder_path + file)
			if not image:
				print("Error: Could not load image:", file)
			data.append(image)
			print(data)
			max_width = max(max_width, image.get_width())
			max_height = max(max_height, image.get_height())
			image_count += 1


	# Create 3D texture
	var texture = ImageTexture3D.new()
	var tex_error = texture.create(Image.FORMAT_RGBA8, max_width, max_height, image_count, false, data)
	print(tex_error)

	var save_path = folder_path + texture_name
	ResourceSaver.save(texture, save_path)

	print("Attempting to set shader params")
	var material = slice_mesh.get_active_material(0)
	material.set_shader_parameter("shader_parameter/texture3D", texture)
	print("Set Shader Params")

	# Free resources
	# dir_access.free()

	print("Successfully created 3D texture with", image_count, "layers")


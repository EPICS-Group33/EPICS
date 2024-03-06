extends Sprite2D

var frame_index = 0
var frame_count = 36

var texture_1 = preload("res://assets/textures/MRI_Sprite/spritesheet.png")
# var texture_2

func _ready():
	texture = texture_1

func _input(event):
	if event is InputEventMouseButton:
		if event.button_index==MOUSE_BUTTON_WHEEL_DOWN:
			frame_index += 1
		elif event.button_index==MOUSE_BUTTON_WHEEL_UP:
			frame_index -= 1


		frame_index = wrapf(frame_index, 0, frame_count)

		frame = frame_index

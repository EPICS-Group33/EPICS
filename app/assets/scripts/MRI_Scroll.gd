extends Sprite2D

var frame_index = 0
var frame_count = 36

func _input(event):
	if event is InputEventMouseButton:
		if event.button_index==MOUSE_BUTTON_WHEEL_DOWN:
			frame_index += 1
		elif event.button_index==MOUSE_BUTTON_WHEEL_UP:
			frame_index -= 1


		frame_index = wrapf(frame_index, 0, frame_count)

		frame = frame_index

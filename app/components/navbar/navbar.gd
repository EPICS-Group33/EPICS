extends Panel

const link_to_website = "https://epics-group33.github.io/EPICS/web/index.html"
const link_to_articles = "https://epics-group33.github.io/EPICS/web/articles.html"
const link_to_github = "https://epics-group33.github.io/EPICS/"

func _ready() -> void:
	pass



func _on_dashboard_button_2_pressed() -> void:
	pass # Replace with function body.


func _on_health_button_pressed() -> void:
	pass # Replace with function body.


func _on_diagnosis_button_2_pressed() -> void:
	pass # Replace with function body.


func _on_history_button_2_pressed() -> void:
	pass # Replace with function body.


func _on_info_button_2_pressed() -> void:
	OS.shell_open(link_to_github)


func _on_articles_button_2_pressed() -> void:
	OS.shell_open(link_to_articles)

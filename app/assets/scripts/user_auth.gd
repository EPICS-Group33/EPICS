extends Control

const WEBID = "AIzaSyCHkXqf1bj29vjHZSvD0-7gl9msgEwAf64"

const SIGNUP_ENDPOINT = "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=" + WEBID
const LOGIN_ENDPOINT = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=" + WEBID

const TEST_POINT = "https://riskpro-bd429-default-rtdb.asia-southeast1.firebasedatabase.app/"

@onready var http = $HTTPRequest

@onready var signup_username : LineEdit = $TabContainer/Signup/MarginContainer/VBoxContainer/Username
@onready var signup_email : LineEdit = $TabContainer/Signup/MarginContainer/VBoxContainer/Email
@onready var signup_password : LineEdit = $TabContainer/Signup/MarginContainer/VBoxContainer/Password
@onready var signup_cpassword : LineEdit = $"TabContainer/Signup/MarginContainer/VBoxContainer/Confirm Password"
@onready var signup_warning : Label = $"TabContainer/Signup/MarginContainer/VBoxContainer/Signup Warning"

@onready var login_username : LineEdit = $TabContainer/Login/MarginContainer/VBoxContainer/Username
@onready var login_password : LineEdit = $TabContainer/Login/MarginContainer/VBoxContainer/Password
@onready var login_warning : Label = $"TabContainer/Login/MarginContainer/VBoxContainer/Login Warning"

func _ready() -> void:
	print("Ready")
	login_warning.text = ""
	signup_warning.text = ""

func _signup():
	signup_warning.text = ""
	signup_password.modulate = Color.WHITE
	signup_cpassword.self_modulate = Color.WHITE
	signup_username.self_modulate = Color.WHITE
	signup_email.self_modulate = Color.WHITE

	if (signup_password != signup_cpassword):
		signup_warning.text = "Password do not match"
		signup_password.self_modulate = Color.RED
		signup_cpassword.self_modulate = Color.RED
		return

	#TODO: Password validation

	var password : String = signup_password.text
	var email : String = signup_email.text
	var username : String = signup_username.text

	http.request(TEST_POINT + username + ".json")

	var result : Array = await http.request_completed as Array

	if (result[1] != 200):
		signup_warning.text = "An error has occured"
		print(result[3].get_string_from_ascii())
	else:
		if (result[3].get_string_from_utf8() != "null"):
			signup_warning.text = "Username already exists"
			signup_username.self_modulate = Color.RED
		else:
			var body = {
				"email": email,
				"password": password
			}
			var headers = ['Content-type: application/json']
			var json = JSON.new()
			http.request(SIGNUP_ENDPOINT, headers, false, HTTPClient.METHOD_POST, json.stringify(body))
			var signup_result = await http.request_completed as Array




func _on_http_request_request_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	var response = JSON.parse_string(body.get_string_from_utf8())
	if (response_code == 200):
		print(response)
	else:
		print(response.error)

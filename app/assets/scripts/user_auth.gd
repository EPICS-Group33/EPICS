extends Control

const WEBID = "AIzaSyCHkXqf1bj29vjHZSvD0-7gl9msgEwAf64"

const SIGNUP_ENDPOINT = "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=" + WEBID
const LOGIN_ENDPOINT = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=" + WEBID

const TEST_POINT = "https://testsystem-"

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

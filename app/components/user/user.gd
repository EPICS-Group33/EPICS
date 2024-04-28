extends Resource
class_name User

var username : String = ""
var email : String = ""
var password : String = ""

var firstname : String = ""
var lastname : String = ""
var age : int = 0 :
	set(input_age):
		age = clamp(input_age, 13, 100)
	get :
		return age

var has_local_record : bool = false

var risk_profile : RiskProfile

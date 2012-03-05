'''import _mysql as mdb
import uuid'''

class User(object):
	#user levels
	banned=-1
	guest=0
	member=10
	mod=20
	admin=30
	def __init__(self):
		self.level=User.guest
		self.json={
			"Command":"",
			"ContextStatus":"Disabled",
			"ContextText":"",
			"CurrentUser":None,
			"EditText":None,
			"SessionId":None,
			"TerminalTitle":"Terminal - "+"Visitor",
			"ClearScreen":False,
			"Exit":False,
			"PasswordField":False,
			"ScrollToBottom":True,
			"DisplayItems":[]
		}

import _mysql as mdb
import uuid

users={} #online users

class User(object):
	#user levels
	banned=-1
	guest=0
	member=10
	mod=20
	admin=30
	def __init__(self,name,password):
		self.login(name,password)
		self.session=str(uuid.uuid4())
		users[self.session]=self
		self.json={
			"Command":"",
			"ContextStatus":"Disabled",
			"ContextText":"",
			"CurrentUser":None,
			"EditText":None,
			"SessionId":self.session,
			"TerminalTitle":"Terminal - "+name,
			"ClearScreen":False,
			"Exit":False,
			"PasswordField":False,
			"ScrollToBottom":True,
			"DisplayItems":[]
		}

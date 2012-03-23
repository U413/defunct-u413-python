import display

cmds={}

class Command(object):
	json={
		"Command":"",
		"ContextText":"",
		"CurrentUser":None,
		"EditText":None,
		"SessionId":None,
		"TerminalTitle":"Terminal - Visitor",
		"ClearScreen":False,
		"Exit":False,
		"PasswordField":False,
		"ScrollToBottom":True,
		"DisplayItems":[]
	}
	def __init__(self,name,description,callback):
		self.name=name.upper()
		self.description=description
		self._callback=callback
		cmds[self.name]=self

	def callback(self,args,user):
		out=self._callback(args,user)
		out["Command"]=self.name
		return out

def respond(cmd,args,user,ashtml=True):
	out=None
	if cmd in cmds:
		out=cmds[cmd].callback(args,user)
	else:
		out=Command.json.copy()
		out.update({"DisplayItems":[display.Item('<span class="error">"%s" is not a valid command or is not available in the current context.</span>'%cmd)]})
	#later on, output tags and check ashtml to convert BBCode to HTML
	return out

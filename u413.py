import sys
import json

from cmds.cmds import *
from user import *
from display import *

#default JSON
djson={
	"Command":"",
	"ContextStatus":"Disabled",
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

def respond(session,cmd,args):
	if cmd=="":
		return json.dumps(djson)
	user=users[session]
	if cmd in cmds:
		if cmds[cmd].level<=user.level:
			return json.dumps(cmds[cmd].response(user,args))
		else:
			tmp=user.json.copy()
			return json.dumps(tmp.update({"Command":cmd,"DisplayItems":[DisplayItem(text='You do not have the authority to use the command "%s"'%cmd)]}))
	else:
		tmp=user.json.copy()
		return json.dumps(tmp.update({"Command":cmd,"DisplayItems":[DisplayItem(text='"%s" is not a recognized command or is not available in the current context'%cmd)]}))

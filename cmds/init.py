import os
import _cmd as cmd
import display

logo=open(os.path.dirname(__file__)+"/logo.txt","r").read()

def cmd_init(user,args):
	tmp=user.json.copy()
	tmp.update({
		"Command":"INITIALIZE",
		"DisplayItems":[
			display.Item(text="Welcome to..."),
			display.Item(text=logo,donttype=True),
			display.Item(text='Type "HELP" to begin.')
		]
	})
	return tmp

cmd.Command("INITIALIZE","Initialize the terminal",cmd_init)

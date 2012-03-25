import command
import display

logo=open("logo.txt","r").read()

def init_func(args,user):
	out=command.Command.json.copy()
	out.update({
		"DisplayItems":[
			display.Item("Welcome to..."),
			display.Item(logo,donttype=True),
			display.Item('<span style="color:#f00;">U413 is currently down for maintenance and is expected to be up by March 25.\n'+str(user.session)+'</span>',donttype=True)
		],
		"ClearScreen":True
	})
	return out

command.Command("INITIALIZE","Initialize the terminal.",init_func)

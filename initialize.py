import command

logo=open("logo.txt","r").read()

def init_func(args):
	out=command.Command.json.copy()
	out.update({
		"DisplayItems":[
			{
				"Text":"Welcome to...",
				"Mute":False,
				"DontType":False
			},{
			
				"Text":logo,
				"Mute":False,
				"DontType":True
			},{
				"Text":'<span style="color:#f00;">U413 is currently down for maintenance and is expected to be up by March 25.</span>',
				"Mute":False,
				"DontType":True
			}
		],
		"Command":"INITIALIZE",
		"ClearScreen":True
	})
	return out

command.Command("INITIALIZE","Initialize the terminal.",init_func)

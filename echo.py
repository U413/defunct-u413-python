import command

def echo_func(args):
	out=command.Command.json.copy()
	out.update({
		"DisplayItems":[{
			"Text":args,
			"Mute":False,
			"DontType":False
		}],
		"Command":"ECHO"
	})
	return out

command.Command("ECHO","Echo a string to the terminal.",echo_func)

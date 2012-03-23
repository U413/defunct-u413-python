import command
import display

def echo_func(args,user):
	out=command.Command.json.copy()
	out.update({
		"DisplayItems":[display.Item(args)]
	})
	return out

command.Command("ECHO","Echo a string to the terminal.",echo_func)

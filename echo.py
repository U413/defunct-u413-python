import command
import display

def echo_func(args):
	out=command.Command.json.copy()
	out.update({
		"DisplayItems":[display.Item(args)]
	})
	return out

command.Command("ECHO","Echo a string to the terminal.",echo_func)

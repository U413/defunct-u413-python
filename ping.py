import command
import display

def ping_func(args,user):
	out=command.Command.json.copy()
	out.update({
		"DisplayItems":[display.Item("PONG "+args)]
	})
	return out

command.Command("PING","Tests whether everything runs fine. In which case it will return PONG and any accompanied text.",ping_func)

import cmd

def cmd_cls(user,args):
	tmp=user.json.copy()
	tmp.update({"Command":"CLS","ClearScreen":True})
	return tmp

Command("CLS","Clears the screen",cmd_exit)

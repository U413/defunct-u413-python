import cmd

def cmd_exit(user,args):
	tmp=user.json.copy()
	tmp.update({"Command":"EXIT","Exit":True})
	return tmp

Command("EXIT","Closes the terminal",cmd_exit)

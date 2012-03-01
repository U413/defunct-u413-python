import cmd
import display

f=open("logo.txt","r")
logo=f.read()
f.close()

def cmd_init(user,args):
	tmp=user.json.copy()
	tmp.update({"Command":"INITIALIZE","DisplayItems":[
		display.DisplayItem(text="Welcome to..."),
		dispaly.DisplayItem(text=logo,donttype=True),
		display.DisplayItem(text='Type "HELP" to begin.')
	])

Command("INITIALIZE","Initialize the terminal",cmd_init)

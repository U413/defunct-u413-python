'''u413 - an open-source BBS/terminal/PI-themed forum
	Copyright (C) 2012 PiMaster
	Copyright (C) 2012 EnKrypt

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU Affero General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU Affero General Public License for more details.

	You should have received a copy of the GNU Affero General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.'''

import user
<<<<<<< HEAD
=======
import display
import database
>>>>>>> 31dd46dea58cff98b0e37e86850d4080466161e3

cmds={}

class Command(object):
	json={
		"Command":"",
		"ContextText":"",
		"CurrentUser":None,
		"EditText":None,
		"SessionId":None,
		"TerminalTitle":"Terminal - Visitor",
		"ClearScreen":False,
		"Exit":False,
		"PasswordField":False,
		"ScrollToBottom":True,
		"DisplayItems":[]
	}
	def __init__(self,name,description,callback,level=user.User.guest,hidden=False):
		self.name=name.upper()
		self.description=description
		self.level=level
		self.callback=callback
		self.hidden=hidden
		cmds[self.name]=self

<<<<<<< HEAD
def respond(cli,u413,ashtml=True):
	u413.donttype("Command: "+u413.user.cmd)
	u413.donttype(str(u413.cmddata))
	cmdarg=cli.split(' ',1)
	cmd=cmdarg[0].upper()
	args=""
	if len(cmdarg)>1:
		args=cmdarg[1]
	if u413.user.cmd=='':
		if cmd in cmds:
			cmds[cmd].callback(args,u413)
		else:
			u413.type('<span class="error">"%s" is not a valid command or is not available in the current context.</span>'%cmd)
	else:
		if cmd.lower()=="cancel":
			#Note: this works because commands must actively request continuation
			u413.type("Action cancelled.")
			u413.set_context("")
		else:
			cmds[u413.user.cmd].callback(cli,u413)
=======
	def callback(self,args,user):
		out=self._callback(args,user)
		out["Command"]=self.name
		return out

def respond(cmd,args,user,ashtml=True):
	out=None
	
	#update history and cmd if context if None. Otherwise it may record sensitive information such as passwords
	if user.context=='':
		user.history.append(cmd)
		user.cmd=cmd
		database.query("UPDATE sessions SET history='%s',cmd='%s' WHERE id='%s';"%(database.escape(str(user.history)),database.escape(user.cmd),user.session))
	
	if user.context!='' and cmd.upper()!="CANCEL":
		out=cmds[user.cmd].callback(cmd,user)
	elif cmd.upper() in cmds:
		if int(cmds[cmd].level)>int(user.level):
			out=Command.json.copy()
			out.update({"DisplayItems":[display.Item('<span class="error">"%s" is not a valid command or is not available in the current context.</span>'%cmd)]})
		else:
			out=cmds[cmd.upper()].callback(args,user)
	else:
		out=Command.json.copy()
		out.update({"DisplayItems":[display.Item('<span class="error">"%s" is not a valid command or is not available in the current context.</span>'%cmd)]})
	#later on, output tags and check ashtml to convert BBCode to HTML
	
	#change title if user is logged in
	if user.username!="Guest":
		out.update({
			"TerminalTitle":"Terminal - "+user.username
		})
	
	return out
>>>>>>> 31dd46dea58cff98b0e37e86850d4080466161e3

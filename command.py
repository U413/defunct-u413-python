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
import database

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

	def callback(self,args,user):
		out=self._callback(args,user)
		out["Command"]=self.name

def respond(cli,u413,ashtml=True):
	cmdarg=cli.split(' ',1)
	cmd=cmdarg[0].upper()
	args=""
	if len(cmdarg)>1:
		args=cmdarg[1]

	#update history and cmd if it's not a command that handles sensitive data
	sensitive=['LOGIN','REGISTER']
	if u413.user.cmd not in sensitive and cmd not in sensitive:
		u413.user.history.append(cmd)
		database.query("UPDATE sessions SET history='%s' WHERE id='%s';"%(database.escape(str(u413.user.history)),u413.user.session))

	if u413.user.cmd=='':
		u413.j["Command"]=cmd
		if cmd in cmds and cmds[cmd].level<=u413.user.level:
			cmds[cmd].callback(args,u413)
		else:
			u413.type('<span class="error">"%s" is not a valid command or is not available in the current context.</span>'%cmd)
	else:
		u413.j["Command"]=u413.user.cmd.upper()
		if cmd=="CANCEL":
			#Note: this works because commands must actively request continuation
			u413.type("Action cancelled.")
			u413.set_context("")
		else:
			cmds[u413.user.cmd.upper()].callback(cli,u413)

	#change title if user is logged in
	if u413.user.name!="Guest":
		u413.set_title("Terminal - "+u413.user.name)

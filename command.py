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
import database as db
import util
import re
import signal

cmds={}

class Command(object):
	def __init__(self,name,usage,args,description,callback,level=user.User.guest,hidden=False):
		self.name=name.upper()
		self.usage=usage
		self.args=args
		self.description=description
		self.level=level
		self.callback=callback
		self.hidden=hidden
		cmds[self.name]=self

class OvertimeException(Exception): pass

def execlimit(function, seconds=4):
	old_handler = signal.getsignal(signal.SIGALRM)
	def new_handler(signum, frame):
		raise OvertimeException(Exception)
	signal.signal(signal.SIGALRM, new_handler)
	signal.alarm(seconds)
	try:
		return function()
	finally:
		signal.alarm(0)
		signal.signal(signal.SIGALRM, old_handler)

aliasout=None

def getaliashelper(a,s,u):
	global aliasout
	m=re.match(a["from"],s)
	if m!=None:
		aliasout=a

def getalias(s,u413):
	for a in u413.user.alias:
		try:
			execlimit(lambda: getaliashelper(a,s,u413))
		except OvertimeException:
			u413.type('Non-terminating regex detected, terminating.')
			break
		if aliasout!=None:
			return aliasout
	return None

c=''

def execaliashelper(a,u):
	global c
	c=re.sub(a["from"],a["to"],c,1)

def execalias(cli,a,u413):
	global c
	c=cli
	try:
		execlimit(lambda: execaliashelper(a,u413))
	except OvertimeException:
		u413.type('None-terminating regex detected, terminating.')
		return
	cmd=c.split(' ')[0].upper()
	#prevent recursion
	if cmd not in cmds:
		u413.type('"%s" is not a valid command or is not available in the current context.'%cmd)
		return
	respond(c,u413)

def respond(cli,u413,ashtml=True):
	cmdarg=cli.split(' ',1)
	cmd=cmdarg[0].upper()
	args=""
	if len(cmdarg)>1:
		args=cmdarg[1]

	#update history and cmd if it's not a command that handles sensitive data
	sensitive=['LOGIN','REGISTER']
	if u413.user.cmd not in sensitive and cmd not in sensitive:
		if args!='':
			u413.user.history.append(cmd+' '+args)
		else:
			u413.user.history.append(cmd)

	if u413.user.cmd=='':
		u413.j["Command"]=cmd
		if cmd in cmds and cmds[cmd].level<=u413.user.level:
			cmds[cmd].callback(args,u413)
		else:
			a=getalias(cli,u413)
			if a!=None:
				execalias(cli,a,u413)
			elif util.isint(cmd):
				if u413.user.context!='TOPIC' and 'TOPIC' in u413.user.context:
					cmds["TOPIC"].callback('%i %i'%(int(u413.user.context.split(' ')[1]),int(cmd)),u413)
				elif u413.user.context!='BOARD' and 'BOARD' in u413.user.context:
					cmds["BOARD"].callback('%s %i'%(u413.user.context.split(' ')[1],int(cmd)),u413)
				else:
					u413.type('"%s" is not a valid command or is not available in the current context.'%cmd)
			else:
				u413.type('"%s" is not a valid command or is not available in the current context.'%cmd)
	else:
		u413.j["Command"]=u413.user.cmd.upper()
		if cmd=="CANCEL":
			#Note: this works because commands must actively request continuation
			u413.type("Action cancelled.")
			u413.set_context("")
		else:
			cmds[u413.user.cmd.upper()].callback(cli,u413)
	
	db.query("UPDATE sessions SET history='%s' WHERE id='%s';"%(db.escape(str(u413.user.history)),u413.user.session))

	#change title if user is logged in
	if u413.user.name!="Guest":
		u413.set_title("Terminal - "+u413.user.name)

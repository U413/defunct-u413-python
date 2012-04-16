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

import command

def htmlify(s):
	return s.replace('<','&lt;').replace('>','&gt;')

def help_func(args,u413):
	if args.strip()=="":
		helpout=''
		u413.type("The following commands are available:")
		u413.donttype("")
		helpout='<table>'
		for cmd in command.cmds:
			if u413.user.level>=u413.cmds[cmd].level and not u413.cmds[cmd].hidden:
				c=u413.cmds[cmd]
				helpout+='<tr><td style="width:2em;"></td><td>'+cmd+'</td><td style="padding-left:1em;">'+command.cmds[cmd].description+"</td></tr>"
		helpout+='</table><br/>[] - optional parameter<br/>&lt;&gt; - required parameter<br/>SHIFT+ENTER to drop down to a new line.'
		u413.donttype(helpout)
	else:
		cmd=args.split()[0].upper()
		if cmd in command.cmds and int(command.cmds[cmd].level)<=int(u413.user.level):
			c=command.cmds[cmd]
			#change this to something that shows a more detailed help
			u413.type(cmd+' - '+c.description)
			u413.donttype("Usage: "+cmd+" "+htmlify(c.usage))
			for a in c.args:
				u413.donttype('<span class="tab"></span>'+a+' - '+c.args[a])
		else:
			u413.type('"%s" is not a command.'%cmd)

command.Command("HELP","[command]",{"command":"An optional command to list help information"},"Prints information about commands.",help_func)

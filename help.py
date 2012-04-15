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

def help_func(args,u413):
	if args.strip()=="":
		helpout=''
		for cmd in command.cmds:
			if u413.user.level>=command.cmds[cmd].level and not command.cmds[cmd].hidden:
				helpout+=cmd+" - "+command.cmds[cmd].description+"<br/>\n"
		u413.donttype(helpout)
		u413.donttype("SHIFT+ENTER to drop down to a new line.")
	else:
		cmd=args.split()[0].upper()
		if cmd in command.cmds and int(command.cmds[cmd].level)<=int(u413.user.level):
			#change this to something that shows a more detailed help
			u413.type("> "+cmd+" - "+command.cmds[cmd].description)
		else:
			u413.type('"%s" is not a command.'%cmd)

command.Command("HELP","Prints information about commands.",help_func)

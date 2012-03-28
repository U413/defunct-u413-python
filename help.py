'''u413 - an open-source BBS/terminal/PI-themed forum
	Copyright (C) 2012 PiMaster
	
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
import display

def help_func(args,user):
	out=command.Command.json.copy()
	if args=="":
		helpout=''
		for cmd in command.cmds:
			if user.level>=command.cmds[cmd].level:
				helpout+=cmd+" - "+command.cmds[cmd].description+"<br>"
		out["DisplayItems"]=[display.Item(helpout,donttype=True),display.Item("SHIFT+ENTER to drop down to a new line.",donttype=True)]
	else:
		cmd=args.split()[0].upper()
		if cmd in command.cmds and command.cmds[cmd].level<=user.level:
			#change this to something that shows a more detailed help
			out["DisplayItems"]=[display.Item("> "+cmd+" - "+command.cmds[cmd].description)]
		else:
			out["DisplayItems"]=[display.Item('"%s" is not a command.'%cmd)]
	return out       

command.Command("HELP","Prints information about commands.",help_func,0)
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

logo=open("logo.txt","r").read()

def init_func(args,user):
	out=command.Command.json.copy()
	out.update({
		"DisplayItems":[
			display.Item("Welcome to..."),
			display.Item(logo,donttype=True),
			display.Item('<span style="color:#f00;">U413 is currently down for maintenance and is expected to be up by March 25.</span>',donttype=True)
		],
		"ClearScreen":True
	})
	return out

command.Command("INITIALIZE","Initialize the terminal.",init_func)

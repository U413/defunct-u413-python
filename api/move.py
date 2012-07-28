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
import database

def isint(i):
	try:
		i=int(i)
	except:
		return False
	return True

def move_func(args,u413):
	args=database.escape(args)
	params=args.split(' ')
	if args=="" or args==" " or len(params)!=2:
		u413.type("Invalid Parameters")
	elif isint(params[0]) and isint(params[1]):
		rows=database.query("SELECT * FROM posts WHERE topic=TRUE AND id=%i;"%int(params[0]))
		checkrows=database.query("SELECT * FROM boards WHERE id=%i;"%int(params[1]))
		if len(rows)==0 or len(checkrows)==0:
			u413.type("Invalid Parameters")
		else:
			database.query("UPDATE posts SET parent=%i WHERE id=%i;"%(int(params[1]),int(params[0])))
			u413.type("Moved topic "+params[0]+" to board "+params[1])
			
	else:
		u413.type("Invalid Parameters")

command.Command("MOVE","<topic id> <board id>",{"topic id":"The id of the topic to move","board id":"The id of the board to move the topic to"},"Allows mods to move a topic to another board",move_func,20)

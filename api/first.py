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
import user

def first_func(args,u413):
	context=u413.user.context.split(' ')
	if context[0]=='BOARD':
		u413.cmds["BOARD"].callback(context[1]+' 1',u413)
	elif context[0]=='TOPIC':
		u413.cmds["TOPIC"].callback(context[1]+' 1',u413)
	else:
		u413.type('"FIRST" is not a valid command or is not available in the current context.')

command.Command("FIRST","",{},"Go to the first page.",first_func,user.User.member)

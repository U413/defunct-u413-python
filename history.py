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
import util

def history_func(args,u413):
	u413.type("User command history:")
	out='<br/><table>'
	for cmd in u413.user.history:
		out+='<tr><td style="width:2em;">'+cmd+'</td></tr>'
	u413.donttype(out+'</table>')

command.Command("HISTORY","",{},"Lists the user's command history.",history_func,user.User.member)

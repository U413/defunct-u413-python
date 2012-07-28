'''u413 - an open-source BBS/terminal/PI-themed forum
	Copyright (C) 2012 PiMaster
	Copyright (C) 2012 EnKrypt

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU Affero General Public License as published by
	the Free Software Foundation, either version 3 of the License,or
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

def who_func(args,u413):
	u413.donttype("Username: "+u413.user.name)
	u413.donttype("User ID: "+str(u413.user.userid))
	u413.donttype("User access: "+user.userlvl(u413.user.level)+' ('+str(u413.user.level)+')')
	u413.donttype("Session ID: "+str(u413.user.session))
	u413.donttype("Session expires: "+util.until(u413.user.expire))

command.Command("WHO","",{},"Output statistics about the currently logged-in user.",who_func)

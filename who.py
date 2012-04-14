'''u413 - an open-source BBS/terminal/PI-themed forum
	Copyright (C) 2012 PiMaster
	Copyright (C) 2012 EnKrypt

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU Affero General Public License as published by
	the Free Software Foundation,either version 3 of the License,or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU Affero General Public License for more details.

	You should have received a copy of the GNU Affero General Public License
	along with this program.  If not,see <http://www.gnu.org/licenses/>.'''

import command

def w_func(args,u413):
	out=command.Command.json.copy()
<<<<<<< HEAD:who.py
	u413.donttype("Username: "+u413.user.username)
	u413.donttype("User ID: "+str(u413.user.userid))
	u413.donttype("Session ID: "+str(u413.user.session))
=======
	out["DisplayItems"]=[
		display.Item("Username: "+user.username,donttype=True),
		display.Item("User ID: "+str(user.userid),donttype=True),
		display.Item("User Access Level: "+str(user.level),donttype=True),
		display.Item("Session ID: "+str(user.session),donttype=True)
	]
	return out
>>>>>>> 31dd46dea58cff98b0e37e86850d4080466161e3:w.py

command.Command("WHO","Output statistics about the currently logged-in user.",w_func)

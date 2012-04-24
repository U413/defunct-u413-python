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
import database as db
import util

def mute_func(args,u413):
	muted=bool(ord(db.query("SELECT muted FROM users WHERE id=%s;"%u413.user.userid)[0]["muted"]))
	db.query("UPDATE users SET muted=%s;"%str(not muted).upper())
	u413.mute=not muted
	if muted:
		u413.type("Terminal unmuted.")
	else:
		u413.type("Terminal muted.")

command.Command("MUTE","",{},"Stops the terminal from making the typing sound.",mute_func,user.User.member)

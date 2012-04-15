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
import database as db

def wall_func(args,u413):
	r=db.query("SELECT * FROM wall;")
	if args.strip()=='':
		if len(r)==0:
			u413.type("There are no notes on the wall.")
		else:
			u413.type("Welcome to the wall!")
			u413.type("")
			for entry in r:
				u=db.query("SELECT username FROM users WHERE id=%i"%int(entry["user"]))
				u413.donttype('{%s} - %s <span class="dim">%s</span>'%(u[0]["username"],entry["text"],str(entry["posted"])))
				u413.set_context("WALL")
			u413.clear_screen()
	else:
		if len(r)>=256:
			db.query("DELETE FROM wall ORDER BY posted LIMIT 1;")
		db.query("INSERT INTO wall(user,text) VALUES(%i,'%s');"%(u413.user.userid,db.escape(args)))
		u413.type("Your note has been posted to the wall.")
		
command.Command("WALL","Access the u413 wall",wall_func,user.User.member)

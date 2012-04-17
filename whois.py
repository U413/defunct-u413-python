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

def whois_func(args,u413):
	args=args.split(' ')[0]
	if len(args)==0:
		u413.cmds["WHO"].callback('',u413)
	else:
		u=db.query("SELECT * FROM users WHERE UCASE(username)='%s';"%db.escape(args.upper()))
		if len(u)==0:
			u413.type('"%s" is not a u413 member.'%util.htmlify(args.upper()))
		else:
			u=u[0]
			s=db.query("SELECT user FROM sessions WHERE user='%s';"%db.escape(u["id"]))
			if len(s)==0:
				s=False
			else:
				s=True
			u413.donttype('Username: '+util.htmlify(u["username"]))
			u413.donttype('User ID: '+u["id"])
			u413.donttype('User access: '+user.userlvl(int(u["access"]))+' ('+u["access"]+')')
			u413.donttype('Logged in: '+str(s))

command.Command("WHOIS","[user]",{"user":"The user whose data you wish to view (defaults to you)"},"List data about a user",whois_func,user.User.member)

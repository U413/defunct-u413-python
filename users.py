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
import user
import database as db
import util
import time

def user_func(args,u413):
	sessions=db.query("SELECT username,expire FROM sessions WHERE DATE_SUB(DATE_SUB(expire,INTERVAL 5 HOUR),INTERVAL 55 MINUTE)>NOW();")
	users=int(db.query("SELECT COUNT(*) FROM users;")[0]["COUNT(*)"])
	u413.type("User statistics:")
	out='<br/>Registered users: %i<br/><br/>Active users:<table>'%users
	for u in sessions:
		out+='<tr><td style="width:2em;"></td><td>%s %s</td></tr>'%(util.htmlify(u["username"]),util.ago(int(time.mktime(time.strptime(u["expire"],'%Y-%m-%d %H:%M:%S')))-6*60*60))
	u413.donttype(out+'</table>')
	u413.clear_screen()
	u413.set_context("")

command.Command("USERS","",{},"Lists user statistics",user_func,user.User.member)

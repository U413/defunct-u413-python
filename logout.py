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
import database as db

def logout_func(args,user):
	out=command.Command.json.copy()
	if user.username!="Guest":
		out.update({
			"DisplayItems":[display.Item(user.logout())]
		})
		db.query("UPDATE sessions SET user=0,username='Guest',access=0,expire=NOW(),context='',cmd='',cmddata='' WHERE id='%s';"%user.session)
	else:
		out.update({
			"DisplayItems":[display.Item("You are not logged in")]
		})
	return out

command.Command("LOGOUT","Logs out a user who is logged into U413",logout_func,10)

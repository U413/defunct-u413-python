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
import database

def cancel_func(args,user):
	out=command.Command.json.copy()
	if user.context=='':
		out.update({
			"DisplayItems":[display.Item("CANCEL cannot be used in the current context")]
		})
	else:
		out.update({
			"DisplayItems":[display.Item("Action cancelled.")]
		})
		database.query("UPDATE sessions SET context='',cmddata='{}' WHERE id='%s';"%(user.session))
	return out

command.Command("CANCEL","Cancels the current action.",cancel_func,0)
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

def login_func(args,user):
	params=args.split(" ")
	out=command.Command.json.copy()
	if len(params)==2:
		out.update({
			"DisplayItems":[display.Item(user.login(params[0],params[1]))]
		})
	else:
		out.update({
			"DisplayItems":[display.Item("Invalid Parameters")]
		})
	return out

command.Command("LOGIN","Logs a user onto U413",login_func)

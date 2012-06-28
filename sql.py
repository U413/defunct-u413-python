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

def sql_func(args,u413):
	result=db.query(args)
	if len(result)==0:
		u413.donttype('Empty set')
		return
	out='<table>'
	for name in result[0]:
		out+='<th>'+name+'</th>'
	for row in result:
		out+='<tr>'
		for col in row:
			out+='<td>'+row[col]+'</td>'
		out+='</tr>'
	out+='</table>'
	u413.donttype(out)

command.Command("SQL","<query>",{'query':"SQL query to execute"},"Execute SQL and return the result",sql_func,user.User.owner)

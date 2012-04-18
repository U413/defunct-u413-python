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
import math

def last_func(args,u413):
	context=u413.user.context.split(' ')
	if context[0]=='BOARD':
		page=0
		if context[1]=='ALL':
			context[1]=0
			page=int(db.query("SELECT COUNT(*) FROM posts WHERE topic=TRUE AND parent IN (SELECT id FROM boards WHERE onall=TRUE);")[0]["COUNT(*)"])
		else:
			page=int(db.query("SELECT COUNT(*) FROM posts WHERE parent=%i AND topic=TRUE;"%int(context[1]))[0]["COUNT(*)"])
		if page==0:
			page=1
		else:
			page=math.ceil(page/10.0)
		u413.cmds["BOARD"].callback('%i %i'%(int(context[1]),page),u413)
	elif context[0]=='TOPIC':
		page=int(db.query("SELECT COUNT(*) FROM posts WHERE parent=%i AND topic=FALSE;"%int(context[1]))[0]["COUNT(*)"])
		if page==0:
			page=1
		else:
			page=math.ceil(page/10.0)
		u413.cmds["TOPIC"].callback('%i %i'%(int(context[1]),page),u413)
	else:
		u413.type('"LAST" is not a valid command or is not available in the current context.')

command.Command("LAST","",{},"Go to the last page.",last_func,user.User.member)

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
import database as db
import user
import util

def plural(i,s):
	if i==1:
		return str(i)+' '+s
	return str(i)+' '+s+'s'

def boards_func(args,u413):
	boards=db.query("SELECT * FROM boards WHERE hidden=FALSE;")
	boardlist="<br/><table>"
	for i in boards:
		topic=db.query("SELECT id,posted FROM posts WHERE parent=%i AND topic=TRUE ORDER BY posted DESC LIMIT 1;"%int(i['id']))
		boardlist+="<tr>"
		if len(topic)>0:
			topic=topic[0]
			count=int(db.query("SELECT COUNT(*) FROM posts WHERE parent=%i AND topic=TRUE;"%int(i['id']))[0]["COUNT(*)"])
			posted=db.query("SELECT posted FROM posts WHERE parent=%i ORDER BY posted DESC LIMIT 1;"%int(topic['id']))
			if len(posted)>0:
				posted=posted[0]["posted"]
				boardlist+='<td>{{<span class="transmit" data-transmit="BOARD {0}">{0}</span>}}'.format(str(i['id']))+'</td><td>'+i['name']+' <span class="dim">%s, last reply %s</span></td>'%(plural(count,'topic'),util.ago(posted))
			else:
				boardlist+='<td>{{<span class="transmit" data-transmit="BOARD {0}">{0}</span>}}'.format(str(i['id']))+'</td><td>'+i['name']+' <span class="dim">%s, last reply %s</span></td>'%(plural(count,'topic'),util.ago(topic["posted"]))
		else:
			boardlist+='<td>{{<span class="transmit" data-transmit="BOARD {0}">{0}</span>}}'.format(str(i['id']))+'</td><td>'+i['name']+' <span class="dim">no topics</span></td>'
		boardlist+="</tr>"
	u413.type("Retrieving list of boards...")
	u413.donttype(boardlist+'</table>')
	u413.clear_screen()
	u413.set_context('')

command.Command("BOARDS","",{},"Displays list of available boards",boards_func,user.User.member)

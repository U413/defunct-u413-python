'''u413 - an open-source BBS/transmit/PI-themed forum
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
import util
import bbcode

def msg_func(args,u413):
	if len(args)==0:
		u413.donttype("Fuck off. You'll get your fancy schmancy multi-part UI when it's not 1:30 in the morning.")
		return
	u413.type("Retrieving message...")
	msg=db.query("SELECT * FROM messages WHERE id=%i;"%int(args))
	if len(msg)==0:
		u413.type("Invalid message ID.")
		return
	msg=msg[0]
	sender=db.query("SELECT username FROM users WHERE id=%i;"%int(msg["sender"]))[0]["username"]
	u413.donttype('{{<span class="transmit" data-transmit="MESSAGE {0}">{0}</span>}} <span class="inverted">{1}</span><br/><span class="dim">Sent by {2} {3}</span><br/><br/>{4}'.format(args,msg["topic"],sender,util.ago(msg["sent"]),bbcode.bbcodify(msg["msg"])))
	u413.clear_screen()
	u413.set_context("MESSAGE "+args)

command.Command("MESSAGE","<id>",{"id":"The ID of the PM"},"Displays a private message.",msg_func,user.User.member)

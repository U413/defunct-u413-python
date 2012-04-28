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

def msg_func(args,u413):
	u413.type("Retrieving messages...")
	msgs=db.query("SELECT * FROM messages WHERE receiver=%i;"%u413.user.userid)
	if len(msgs)==0:
		u413.type("You have no messages.")
		return
	out='<table>'
	for msg in msgs:
		user=db.query("SELECT username FROM users WHERE id=%i;"%int(msg["sender"]))[0]["username"]
		if bool(ord(msg["seen"])):
			out+='<tr><td>{%i} %s</td><td>Sent by %s %s</td></tr>'%(int(msg["id"]),msg["topic"],user,util.ago(msg["sent"]))
		else:
			out+='<tr><td>{%i}</td><td><b>%s</b> <span class="dim">sent by %s %s</span></td></tr>'%(int(msg["id"]),msg["topic"],user,util.ago(msg["sent"]))
	out+='</table>'
	u413.set_context("MESSAGES")
	u413.donttype(out)
	u413.clear_screen()

command.Command("MESSAGES","",{},"Displays all received private messages.",msg_func,user.User.member)

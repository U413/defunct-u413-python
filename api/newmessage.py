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

def user_id(uname):
	user=db.query("SELECT username,id FROM users WHERE LCASE(username)='%s';"%db.escape(uname.lower()))
	if len(user)==0:
		return None
	return int(user[0]["id"])

def user_exists(uname):
	user=user_id(uname)
	if user==None:
		return False
	return True

def nmsg_func(args,u413):
	if "step" in u413.cmddata:
		if u413.cmddata["step"]==1:
			u413.cmddata["step"]=2
			args=args.strip().split()[0]
			to=user_id(args)
			if to==None:
				u413.type('"%s" is not a u413 user.'%args)
				return
			u413.cmddata["to"]=to
			u413.type("Enter the topic:")
			u413.set_context("TOPIC")
			u413.continue_cmd()
		elif u413.cmddata["step"]==2:
			u413.cmddata["step"]=3
			u413.cmddata["topic"]=args
			u413.type("Enter your message:")
			u413.set_context("MESSAGE")
			u413.continue_cmd()
		elif u413.cmddata["step"]==3:
			db.query("INSERT INTO messages(sender,receiver,topic,msg,sent,seen) VALUES(%i,%i,'%s','%s',NOW(),FALSE);"%(u413.user.userid,u413.cmddata["to"],db.escape(u413.cmddata["topic"]),db.escape(args)))
			u413.type("Message sent.")
			u413.set_context('')
	else:
		params=args.split(' ',1)
		if len(args)==0:
			u413.cmddata["step"]=1
			u413.type("Enter the receiver:")
			u413.set_context("USER")
			u413.continue_cmd()
		elif len(params)==1:
			u413.cmddata["step"]=2
			args=params[0].strip().split()[0]
			to=user_id(args)
			if to==None:
				u413.type('"%s" is not a u413 user.'%args)
				return
			u413.cmddata["to"]=to
			u413.type("Enter the topic:")
			u413.set_context("TOPIC")
			u413.continue_cmd()
		else:
			u413.cmddata["step"]=3
			args=params[0].strip().split()[0]
			to=user_id(args)
			if to==None:
				u413.type('"%s" is not a u413 user.'%args)
				return
			u413.cmddata["to"]=to
			u413.cmddata["topic"]=params[1]
			u413.type("Enter your message:")
			u413.set_context("MESSAGE")
			u413.continue_cmd()

command.Command("NEWMESSAGE","[user [topic]]",{"id":"The ID of the PM"},"Sends a private message to another user.",nmsg_func,user.User.member)

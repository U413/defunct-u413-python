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

def isint(i):
	try:
		i=int(i)
	except:
		return False
	return True

def newtopic_func(args,u413):
	params=args.split(' ',1)
	#continued NEWTOPIC
	if "step" in u413.cmddata:
		if args=='':
			u413.type("Action cancelled.")
			return
		#BOARD>
		if u413.cmddata["step"]==1:
			if isint(args):
				u413.cmddata["step"]=2
				u413.cmddata["board"]=args
				u413.type("Enter the topic's title:")
				u413.set_context("TITLE")
				u413.continue_cmd()
			else:
				u413.donttype('<span class="error">Invalid board ID</span>')
		#TITLE>
		elif u413.cmddata["step"]==2:
			u413.cmddata["step"]=3
			u413.cmddata["title"]=args
			u413.type("Enter the topic's body:")
			u413.set_context("BODY")
			u413.continue_cmd()
		#BODY>
		elif u413.cmddata["step"]==3:
			db.query("INSERT INTO posts (topic,title,parent,owner,editor,post,locked,edited,posted) VALUES(TRUE,'%s',%i,%i,0,'%s',FALSE,NULL,NOW());"%(db.escape(u413.cmddata["title"]),int(u413.cmddata["board"]),u413.user.userid,db.escape(args)))
			topic=int(db.query("SELECT id FROM posts ORDER BY id DESC LIMIT 1;")[0]["id"])
			u413.type("Topic %i was created successfully."%topic)
	#first use
	else:
		#NEWTOPIC
		if args.strip()=='':
			if "BOARD" in u413.user.context:
				u413.cmddata["step"]=2
				u413.cmddata["board"]=int(u413.user.context[6:])
				u413.type("Enter the topic's title:")
				u413.set_context("TITLE")
			else:
				u413.cmddata["step"]=1
				u413.type("Enter the board ID:")
				u413.set_context("BOARD")
			u413.continue_cmd()
		#NEWTOPIC board
		elif len(params)==1:
			if isint(params[0]):
				u413.cmddata["step"]=2
				u413.cmddata["board"]=int(params[0])
				u413.type("Enter the topic's title:")
				u413.set_context("TITLE")
				u413.continue_cmd()
			else:
				u413.donttype('<span class="error">Invalid board ID</span>')
		#NEWTOPIC board topic
		else:
			if isint(params[0]):
				u413.cmddata["step"]=3
				u413.cmddata["board"]=int(params[0])
				u413.cmddata["topic"]=params[1]
				u413.type("Enter the topic's body:")
				u413.set_context("BODY")
				u413.continue_cmd()
			else:
				u413.donttype('<span class="error">Invalid board ID</span>')

command.Command("NEWTOPIC","[board [title]]",{"board":"The board the topic should be in","title":"The topic's title"},"Create a new topic in either the current or given board.",newtopic_func,user.User.member)

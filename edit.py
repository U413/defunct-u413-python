'''u413 - an open-source BBS/terminal/PI-themed forum
	Copyright (C) 2012 PiMaster
	Copyright (C) 2012 EnKrypt

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU Affero General Public License as published by
	the Free Software Foundation,either version 3 of the License,or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU Affero General Public License for more details.

	You should have received a copy of the GNU Affero General Public License
	along with this program.  If not,see <http://www.gnu.org/licenses/>.'''

import command
import database as db
import user

def isint(i):
	try:
		i=int(i)
	except:
		return False
	return True

def edit_func(args,u413):
	#EDIT already requested continuation
	if "step" in u413.cmddata:
		#ID>
		if u413.cmddata["step"]==1:
			u413.donttype('"'+args+'"')
			if isint(args):
				u413.cmddata["id"]=int(args)
				u413.cmddata["step"]=2
				u413.set_context("NEW BODY")
				u413.type("Enter the new post body:")
				u413.edit_text(db.query("SELECT post FROM posts WHERE id=%i;"%int(args))[0]["post"])
				u413.continue_cmd()
			else:
				u413.type("Invalid post ID.")
				u413.set_context("")
		#NEW BODY>
		elif u413.cmddata["step"]==2:
			post=int(db.query("SELECT owner FROM posts WHERE id=%i;"%u413.cmddata["id"])[0]["owner"])
			owner=int(db.query("SELECT access FROM users WHERE id=%i;"%post)[0]["access"])
			if post!=u413.user.userid:
				if u413.user.level<user.User.halfmod or u413.user.level<=owner:
					u413.type("You do not have permission to edit other user's posts.")
					return
			db.query("UPDATE posts SET post='%s',editor=%i,edited=NOW() WHERE id=%i;"%(db.escape(args),u413.user.userid,u413.cmddata["id"]))
			u413.type("Post edited successfully.")
			u413.set_context("")
	#EDIT used for the first time
	else:
		params=args.split(' ',1)
		#EDIT
		if len(args)==0:
			u413.cmddata["step"]=1
			u413.type("Enter the post's ID:")
			u413.set_context("Post ID")
			u413.continue_cmd()
		#EDIT id
		elif len(params)==1:
			if isint(args):
				u413.cmddata["step"]=2
				u413.cmddata["id"]=int(args)
				u413.type("Enter the new post body:")
				u413.set_context("NEW BODY")
				u413.edit_text(db.query("SELECT post FROM posts WHERE id=%i;"%int(args))[0]["post"])
				u413.continue_cmd()
			else:
				u413.type("Invalid post ID.")
		#EDIT id body
		else:
			if isint(params[0]):
				post=int(db.query("SELECT owner FROM posts WHERE id=%i;"%int(params[0]))[0]["owner"])
				owner=int(db.query("SELECT access FROM users WHERE id=%i;"%post)[0]["access"])
				if post!=u413.user.userid:
					if u413.user.level<user.User.halfmod or u413.user.level<=owner:
						u413.type("You do not have permission to edit other user's posts.")
						return
				db.query("UPDATE posts SET post='%s',editor=%i,edited=NOW() WHERE id=%i;"%(db.escape(params[1]),u413.user.userid,int(params[0])))
				u413.type("Post edited successfully.")
				u413.set_context("")
			else:
				u413.type("Invalid post ID.")

command.Command("EDIT","[id [newtext]]",{"id":"The post ID that you wish to edit","newtext":"The new text for the post"},"Edits a post (reply/topic).",edit_func,user.User.member)

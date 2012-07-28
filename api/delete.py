'''u413 - an open-source BBS/terminal/PI-themed forum
	Copyright (C) 2012 PiMaster
	Copyright (C) 2012 EnKrypt

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU Affero General Public License as published by
	the Free Software Foundation, either version 3 of the License,or
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
import util

def delete_func(args,u413):
	#DELETE already requested continuation
	if "step" in u413.cmddata:
		#ID>
		post=int(db.query("SELECT owner FROM posts WHERE id=%i;"%int(args))[0]["owner"])
		owner=int(db.query("SELECT access FROM users WHERE id=%i;"%post)[0]["access"])
		if post!=u413.user.userid:
			if u413.user.level<user.User.mod or u413.user.level<=owner:
				u413.type("You do not have permission to edit other user's posts.")
				return
		db.query("DELETE FROM posts WHERE id=%i;"%int(args))
		u413.type("Post deleted.")
	#DELETE used for the first time
	else:
		params=args.split(' ',1)
		#DELETE
		if len(args)==0:
			u413.cmddata["step"]=1
			u413.type("Enter the post's ID:")
			u413.set_context("Post ID")
			u413.continue_cmd()
		#DELETE id
		else:
			if util.isint(args):
				post=int(db.query("SELECT owner FROM posts WHERE id=%i;"%int(args))[0]["owner"])
				owner=int(db.query("SELECT access FROM users WHERE id=%i;"%post)[0]["access"])
				if post!=u413.user.userid:
					if u413.user.level<user.User.halfmod or u413.user.level<=owner:
						u413.type("You do not have permission to edit other user's posts.")
						return
				db.query("DELETE FROM posts WHERE id=%i;"%int(args))
				u413.type("Post deleted.")
			else:
				u413.type("Invalid post ID")

command.Command("DELETE","[id]",{"id":"The ID of the post you wish to delete"},"Delete a post.",delete_func,user.User.member)

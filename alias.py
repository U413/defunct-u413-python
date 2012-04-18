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

def alias_func(args,u413):
	if "step" in u413.cmddata:
		if u413.cmddata["step"]==1:
			u413.cmddata["step"]=2
			u413.cmddata["to"]=args
			u413.type("Enter the pattern to be replaced:")
			u413.set_context("FROM")
			u413.continue_cmd()
		elif u413.cmddata["step"]==2:
			u413.user.alias.append({"to":u413.cmddata["to"],"from":args})
			db.query("UPDATE users SET alias='%s' WHERE id=%i;"%(db.escape(repr(u413.user.alias)),u413.user.userid))
			u413.type("Alias created successfully.")
			u413.set_context(u413.cmddata["context"])
		elif u413.cmddata["step"]==3:
			x=None
			for a in range(len(u413.user.alias)):
				if args.upper()==u413.user.alias[a]["from"].upper():
					x=a
			if x==None:
				u413.type('"%s" is not an alias.'%args)
			else:
				del u413.user.alias[x]
				db.query("UPDATE users SET alias='%s' WHERE id=%i;"%(db.escape(repr(u413.user.alias)),u413.user.userid))
				u413.type("Alias deleted.")
				u413.set_context(u413.cmddata["context"])
	else:
		params=args.split(' ',1)
		#ALIAS
		if len(args.split(' ',1)[0])==0:
			aliases=eval(db.query("SELECT alias FROM users WHERE id=%i;"%u413.user.userid)[0]["alias"])
			if len(aliases)==0:
				u413.type("You have no aliases.")
			else:
				u413.type("Your aliases:")
				out='<table>'
				for alias in aliases:
					out+='<tr><td style="width:2em;"></td><td>%s -> %s</td></tr>'%(util.htmlify(alias["from"]),util.htmlify(alias["to"]))
				u413.donttype(out+'</table>')
		#ALIAS to | --delete | --new
		elif len(params)==1:
			if params[0].upper()=="--DELETE":
				u413.cmddata["step"]=3
				u413.cmddata["context"]=u413.user.context
				u413.type("Enter the pattern to be deleted:")
				u413.set_context("PATTERN")
				u413.continue_cmd()
			elif params[0].upper()=="--NEW":
				u413.cmddata["step"]=1
				u413.cmddata["context"]=u413.user.context
				u413.type("Enter the command to alias:")
				u413.set_context("TO")
				u413.continue_cmd()
			else:
				u413.cmddata["step"]=2
				u413.cmddata["context"]=u413.user.context
				u413.cmddata["to"]=params[0]
				u413.type("Enter the pattern to be replaced:")
				u413.set_context("FROM")
				u413.continue_cmd()
		#ALIAS to from | --delete from
		else:
			if params[0].upper()=="--DELETE":
				x=None
				for a in range(len(u413.user.alias)):
					if params[1].upper()==u413.user.alias[a]["from"].upper():
						x=a
				if x==None:
					u413.type('"%s" is not an alias.'%params[1])
				else:
					del u413.user.alias[x]
					u413.donttype(u413.user.alias)
					db.query("UPDATE users SET alias='%s' WHERE id=%i;"%(db.escape(repr(u413.user.alias)),u413.user.userid))
					u413.type("Alias deleted.")
			else:
				u413.user.alias.append({"to":params[0],"from":params[1]})
				db.query("UPDATE users SET alias='%s' WHERE id=%i;"%(db.escape(repr(u413.user.alias)),u413.user.userid))
				u413.type("Alias created successfully.")

command.Command("ALIAS","[[--new] | [to] [from] | [--delete] [to]]",{"--new":"Force ALIAS to prompt (allows for aliases with spaces)","to":"The regex to replace from","from":"The pattern to replace","--delete":"Delete the alias"},"Make an alias of a command.",alias_func,user.User.member)

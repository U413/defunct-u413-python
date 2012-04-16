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

def isint(i):
	try:
		i=int(i)
	except:
		return False
	return True

def output_board(board,page,u413):
	output=''
	if board==0:
		u413.type("Retrieving all topics...")
		t=db.query("SELECT * FROM posts WHERE topic=TRUE LIMIT %i,10;"%((page-1)*10))
		c=int(db.query("SELECT COUNT(*) FROM posts WHERE topic=TRUE;")[0]["COUNT(*)"])
		if c==0:
			u413.donttype('{0} <span class="inverted">BOARD ALL</span> Page %i/1<br/>\n'%page)
		else:
			u413.donttype('{0} <span class="inverted">BOARD ALL</span> Page %i/%i<br/>\n'%(page,math.ceil(c/10.0)))
		output='<table>'
		for topic in t:
			r=int(db.query("SELECT COUNT(*) FROM posts WHERE parent=%i AND topic=FALSE;"%int(topic["id"]))[0]["COUNT(*)"])
			u=db.query("SELECT username FROM users WHERE id=%i;"%int(topic["owner"]))[0]["username"]
			output+='<tr><td style="text-align:right;width:64px;">{%i}</td><td style="padding-left:8px;"><b>%s</b> | <span class="dim">%i replies</span><br/><span class="dim">by %s on %s</td></tr>'%(int(topic["id"]),topic["title"],r,u,str(topic["posted"]))
		if page==1:
			u413.set_context("BOARD ALL")
		else:
			u413.set_context("BOARD ALL %i"%page)
	else:
		b=db.query("SELECT * FROM boards WHERE id=%i;"%board)[0]
		t=db.query("SELECT * FROM posts WHERE parent=%i AND topic=TRUE LIMIT %i,10;"%(board,(page-1)*10))
		c=int(db.query("SELECT COUNT(*) FROM posts WHERE parent=%i AND topic=TRUE;"%board)[0]["COUNT(*)"])
		u413.type("Retrieving board topics...")
		if c==0:
			u413.donttype('{%i} <span class="inverted">%s</span> Page %i/1<br/>\n'%(board,b["name"],page))
		else:
			u413.donttype('{%i} <span class="inverted">%s</span> Page %i/%i<br/>\n'%(board,b["name"],page,math.ceil(c/10.0)))
		output='<table>'
		for topic in t:
			r=int(db.query("SELECT COUNT(*) FROM posts WHERE parent=%i AND topic=FALSE;"%int(topic["id"]))[0]["COUNT(*)"])
			u=db.query("SELECT username FROM users WHERE id=%i;"%int(topic["owner"]))[0]["username"]
			output+='<tr><td style="text-align:right;width:64px;">{%i}</td><td style="padding-left:8px;"><b>%s</b> | <span class="dim">%i replies</span><br/><span class="dim">by %s on %s</td></tr>'%(int(topic["id"]),topic["title"],r,u,str(topic["posted"]))
		if page==1:
			u413.set_context("BOARD %i"%board)
		else:
			u413.set_context("BOARD %i %i"%(board,page))
	u413.donttype(output)

def board_func(args,u413):
	args=args.split(' ')
	if len(args)==0:
		u413.donttype('<span class="error">Invalid board ID.</span>')
	#BOARD id
	elif len(args)==1:
		if args[0].upper()=="ALL":
			args[0]=0
		if isint(args[0]):
			output_board(int(args[0]),1,u413)
			u413.clear_screen()
		else:
			u413.donttype('<span class="error">Invalid board ID</span>')
	#BOARD id page
	else:
		if args[0].upper()=="ALL":
			args[0]=0
		if not isint(args[1]):
			args[1]=1
		if isint(args[0]):
			output_board(args[0],args[1],u413)
			u413.clear_screen()
		else:
			u413.donttype('<span class="error">Invalid board ID</span>')

command.Command("BOARD","<id> [page]",{"id":"The id of the board to view"},"Show the most recent topics in a board.",board_func,user.User.member)

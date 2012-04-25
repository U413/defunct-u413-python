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
import util

def output_board(board,page,u413):
	if board==403:
		u413.type("Access denied.")
		return
	output=''
	if board==0:
		u413.type("Retrieving all topics...")
		c=int(db.query("SELECT COUNT(*) FROM posts WHERE topic=TRUE AND parent IN (SELECT id FROM boards WHERE onall=TRUE);")[0]["COUNT(*)"])
		if c==0 or page<1:
			page=1
		elif page>math.ceil(c/10.0):
			page=math.ceil(c/10.0)
		t=db.query("SELECT *,id AS t FROM posts WHERE topic=TRUE AND parent IN (SELECT id FROM boards WHERE onall=TRUE) ORDER BY (SELECT MAX(posted) FROM posts WHERE topic=FALSE AND parent=t OR topic=TRUE AND id=t) DESC LIMIT %i,10;"%((page-1)*10))[::-1]
		if c==0:
			output+='{{<span class="transmit" data-transmit="BOARD 0">0</span>}} <span class="inverted">BOARD ALL</span> Page {0}/1<br/>'.format(page)
		else:
			output+='{{<span class="transmit" data-transmit="BOARD 0">0</span>}} <span class="inverted">BOARD ALL</span> Page {0}/{1}<br/>'.format(page,math.ceil(c/10.0))
		output+='<table>'
		for topic in t:
			r=int(db.query("SELECT COUNT(*) FROM posts WHERE parent=%i AND topic=FALSE;"%int(topic["id"]))[0]["COUNT(*)"])
			if topic["parent"]=='4':
				last=''
				anons=db.query("SELECT DISTINCT owner FROM (SELECT owner,posted FROM (SELECT owner,posted FROM posts WHERE topic=FALSE AND parent=%i) AS t1 GROUP BY owner ORDER BY posted) AS t2;"%int(topic["id"]))
				if r!=0:
					last=db.query("SELECT owner,posted FROM posts WHERE parent=%i AND topic=FALSE ORDER BY posted DESC LIMIT 1;"%int(topic["id"]))[0]
					lastu=util.anoncode(anons,last["owner"],topic["owner"])
					last=' | last reply by {0} {1}'.format(lastu,util.ago(last["posted"]))
				output+='<tr><td>{{<span class="transmit" data-transmit="BOARD {0}">{0}</span>}}</td><td style="text-align:right;width:64px;">{{<span class="transmit" data-transmit="TOPIC {1}">{1}</span>}}</td><td style="padding-left:8px;"><b>{2}</b> <span class="dim">by OP {3}</span><br/><span class="dim">{4} replies{5}</span><br/></td></tr>'.format(topic["parent"],topic["id"],topic["title"],util.ago(topic["posted"]),r,last)
			else:
				last=''
				if r!=0:
					last=db.query("SELECT owner,posted FROM posts WHERE parent=%i AND topic=FALSE ORDER BY posted DESC LIMIT 1;"%int(topic["id"]))[0]
					lastu=db.query("SELECT username FROM users WHERE id=%i;"%int(last["owner"]))[0]["username"]
					last=' | last reply by <span class="transmit" data-transmit="WHOIS {0}">{0}</span> {1}'.format(lastu,util.ago(last["posted"]))
				u=db.query("SELECT username FROM users WHERE id=%i;"%int(topic["owner"]))[0]["username"]
				output+='<tr><td>{{<span class="transmit" data-transmit="BOARD {0}">{0}</span>}}</td><td style="text-align:right;width:64px;">{{<span class="transmit" data-transmit="TOPIC {1}">{1}</span>}}</td><td style="padding-left:8px;"><b>{2}</b> <span class="dim">by <span class="transmit" data-transmit="WHOIS {3}">{3}</span> {4}</span><br/><span class="dim">{5} replies{6}</span><br/></td></tr>'.format(topic["parent"],topic["id"],topic["title"],u,util.ago(topic["posted"]),r,last)
		if page==1:
			u413.set_context("BOARD ALL")
		else:
			u413.set_context("BOARD ALL %i"%page)
	else:
		b=db.query("SELECT * FROM boards WHERE id=%i;"%board)
		if len(b)==0:
			u413.type("Board %i does not exist."%board)
			return
		else:
			b=b[0]
		c=int(db.query("SELECT COUNT(*) FROM posts WHERE parent=%i AND topic=TRUE;"%board)[0]["COUNT(*)"])
		if c==0 or page<1:
			page=1
		elif page>math.ceil(c/10.0):
			page=math.ceil(c/10.0)
		t=db.query("SELECT *,id as t FROM posts WHERE topic=TRUE AND parent=%i ORDER BY (SELECT MAX(posted) FROM posts WHERE topic=FALSE AND parent=t OR topic=TRUE AND id=t) ASC LIMIT %i,10;"%(board,(page-1)*10))
		u413.type("Retrieving board topics...")
		if c==0:
			output+='{{<span class="transmit" data-transmit="BOARD {0}">{0}</span>}} <span class="inverted">{1}</span> Page {2}/1<br/>'.format(board,b["name"],page)
		else:
			output+='{{<span class="transmit" data-transmit="BOARD {0}">{0}</span>}} <span class="inverted">{1}</span> Page {2}/{3}<br/>'.format(board,b["name"],page,int(math.ceil(c/10.0)))
		output+='<table>'
		if board==4:
			for topic in t:
				r=int(db.query("SELECT COUNT(*) FROM posts WHERE parent=%i AND topic=FALSE;"%int(topic["id"]))[0]["COUNT(*)"])
				if r!=0:
					last=db.query("SELECT MAX(posted) AS posted FROM posts WHERE parent=%i AND topic=FALSE;"%int(topic["id"]))[0]
					last=' | last reply %s'%util.ago(last["posted"])
				output+='<tr><td style="text-align:right;width:64px;">{{<span class="transmit" data-transmit="TOPIC {0}">{0}</span>}}</td><td style="padding-left:8px;"><b>{1}</b> <span class="dim">by OP {2}</span><br/><span class="dim">{3} replies{4}</span><br/></td></tr>'.format(int(topic["id"]),topic["title"],util.ago(topic["posted"]),r,last)
		else:
			for topic in t:
				r=int(db.query("SELECT COUNT(*) FROM posts WHERE parent=%i AND topic=FALSE;"%int(topic["id"]))[0]["COUNT(*)"])
				last=''
				if r!=0:
					last=db.query("SELECT MAX(posted) AS posted,owner FROM posts WHERE parent=%i AND topic=FALSE;"%int(topic["id"]))[0]
					lastu=db.query("SELECT username FROM users WHERE id=%i;"%int(last["owner"]))[0]["username"]
					last=' | last reply by <span class="transmit" data-transmit="WHOIS {0}">{0}</span> {1}'.format(lastu,util.ago(last["posted"]))
				u=db.query("SELECT username FROM users WHERE id=%i;"%int(topic["owner"]))[0]["username"]
				output+='<tr><td style="text-align:right;width:64px;">{{<span class="transmit" data-transmit="TOPIC {0}">{0}</span>}}</td><td style="padding-left:8px;"><b>{1}</b> <span class="dim">by <span class="transmit" data-transmit="WHOIS {2}">{2}</span> {3}</span><br/><span class="dim">{4} replies{5}</span><br/></td></tr>'.format(int(topic["id"]),topic["title"],u,util.ago(topic["posted"]),r,last)
		if page==1:
			u413.set_context("BOARD %i"%board)
		else:
			u413.set_context("BOARD %i %i"%(board,page))
	u413.donttype(output)
	if board==666:
		u413.exec_js('$("#frame").addClass("hell");$(".backgroundImage").attr("src","content/hellbg.png").css("opacity",0.9);','$("#frame").removeClass("hell");$(".backgroundImage").attr("src","content/background.jpg").css("opacity",0.1);')
	u413.clear_screen()

def board_func(args,u413):
	args=args.split(' ')
	if len(args)==0:
		u413.type('Invalid board ID.')
	#BOARD id
	elif len(args)==1:
		if args[0].upper()=="ALL":
			args[0]=0
		if util.isint(args[0]):
			output_board(int(args[0]),1,u413)
		else:
			u413.type('Invalid board ID.')
	#BOARD id page
	else:
		if args[0].upper()=="ALL":
			args[0]=0
		if args[1].upper()=='LAST':
			args[1]=int(db.query("SELECT COUNT(*) FROM posts WHERE parent=%i AND topic=TRUE;"%int(args[0]))[0]["COUNT(*)"])
			if args[1]==0:
				args[1]=1
			else:
				args[1]=math.ceil(args[1]/10.0)
		elif not util.isint(args[1]):
			args[1]=1
		else:
			args[1]=int(args[1])
		output_board(int(args[0]),args[1],u413)

command.Command("BOARD","<id> [page]",{"id":"The id of the board to view"},"Show the most recent topics in a board.",board_func,user.User.member)

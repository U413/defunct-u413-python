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

'''
+--------+--------------+------+-----+---------+----------------+
| Field  | Type         | Null | Key | Default | Extra          |
+--------+--------------+------+-----+---------+----------------+
| id     | int(11)      | NO   | PRI | NULL    | auto_increment |
| topic  | bit(1)       | YES  |     | NULL    |                |
| title  | varchar(128) | YES  |     | NULL    |                |
| parent | int(11)      | YES  |     | NULL    |                |
| owner  | int(11)      | YES  |     | NULL    |                |
| editor | int(11)      | YES  |     | NULL    |                |
| post   | text         | YES  |     | NULL    |                |
| locked | bit(1)       | YES  |     | NULL    |                |
| edited | datetime     | YES  |     | NULL    |                |
| posted | datetime     | YES  |     | NULL    |                |
+--------+--------------+------+-----+---------+----------------+
'''

import command
import user
import database as db
import math
import bbcode
import util

def output_page(topic,page,u413):
	t=db.query("SELECT * FROM posts WHERE id=%i AND topic=TRUE;"%topic)
	if len(t)==0:
		u413.type("Invalid topic ID.")
		return
	t=t[0]
	b=db.query("SELECT name FROM boards WHERE id=%i;"%int(t["parent"]))[0]["name"]#board name
	c=int(db.query("SELECT COUNT(*) FROM posts WHERE parent=%i;"%topic)[0]["COUNT(*)"])#number of replies
	if page==0 and page>1 or page!=0 and page>math.ceil(c/10.0):
		page=math.ceil(c/10.0)
	if page<1:
		page=1
	r=db.query("SELECT * FROM posts WHERE parent=%i ORDER BY id LIMIT %i,10;"%(topic,(page-1)*10))#replies
	u413.type("Retreiving topic...")
	if t["parent"]=='4':
		u413.donttype('{{<span class="transmit" data-transmit="BOARD 4">4</span>}} {0} {{<span class="transmit" data-transmit="TOPIC {1}">{1}</span>}} <span class="inverted">{2}</span><br/><span class="dim">Posted by OP {3}<br/>'.format(b,topic,t["title"],util.ago(t["posted"])))
		e=db.query("SELECT username FROM users WHERE id=%i;"%int(t["editor"]))
		if len(e)==0:
			u413.donttype(bbcode.bbcodify(t["post"])+'<br/>')
		else:
			u413.donttype(bbcode.bbcodify(t["post"])+'<br/><br/><i>Edited by <span class="transmit" data-transmit="WHOIS {0}>{0}</span> {1}</i><br/>'.format(e[0]["username"],util.ago(t["posted"])))
	else:
		u=db.query("SELECT username FROM users WHERE id=%i;"%int(t["owner"]))[0]["username"]#username
		u413.donttype('{{<span class="transmit" data-transmit="BOARD {0}">{0}</span>}} {1} {{<span class="transmit" data-transmit="TOPIC {2}">{2}</span>}} <span class="inverted">{3}</span><br/><span class="dim">Posted by <span class="transmit" data-transmit="WHOIS {4}">{4}</span> {5}<br/>'.format(int(t["parent"]),b,topic,t["title"],u,util.ago(t["posted"])))
		e=db.query("SELECT username FROM users WHERE id=%i;"%int(t["editor"]))
		if len(e)==0:
			u413.donttype(bbcode.bbcodify(t["post"])+'<br/>')
		else:
			u413.donttype(bbcode.bbcodify(t["post"])+'<br/><br/><i>Edited by <span class="transmit" data-transmit="WHOIS {0}>{0}</span> {1}</i><br/>'.format(e[0]["username"],util.ago(t["posted"])))
	if c==0:
		u413.donttype('Page 1/1<br/>')
	else:
		u413.donttype('Page %i/%i<br/>'%(page,math.ceil(c/10.0)))
	if c==0:
		u413.type("There are no replies.")
	else:
		if t['parent']=='4':
			anons=db.query("SELECT DISTINCT owner FROM (SELECT owner,posted FROM (SELECT owner,posted FROM posts WHERE topic=FALSE AND parent=%i) AS t1 GROUP BY owner ORDER BY posted) AS t2;"%topic)
			for reply in r:
				owner=util.anoncode(anons,reply["owner"],t["owner"])
				editor=db.query("SELECT username FROM users WHERE id=%i;"%int(reply["editor"]))
				if len(editor)==0:
					u413.donttype('<table><tr><td>&gt;</td><td style="text-align:center;width:160px;border-right:solid 1px lime;"><span class="transmit" data-transmit="WHOIS {0}">{0}</span></td><td style="padding-left:8px;padding-right:8px;">{{<span class="transmit" data-transmit="[quote]{1}[/quote]">{1}</span>}}<br/>{2}<br/><br/><span class="dim">Posted {3}</span></td></tr></table><br/>'.format(owner,int(reply["id"]),bbcode.bbcodify(reply["post"]),util.ago(reply["posted"])))
				else:
					editor=owner
					if reply["editor"]!=reply["owner"]:
						editor=editor[0]["username"]
					u413.donttype('<table><tr><td>&gt;</td><td style="text-align:center;width:160px;border-right:solid 1px lime;"><span class="transmit" data-transmit="WHOIS {0}">{0}</span></td><td style="padding-left:8px;padding-right:8px;">{{<span class="transmit" data-transmit="[quote]{1}[/quote]">{1}</span>}}<br/>{2}<br/><br/><i>Edited by <span class="transmit" data-transmit="WHOIS {3}">{3}</span> {4}</i><br/><span class="dim">Posted {5}</span></td></tr></table><br/>'.format(owner,int(reply["id"]),bbcode.bbcodify(reply["post"]),editor,util.ago(reply["edited"]),util.ago(reply["posted"])))
		else:
			for reply in r:
				owner=db.query("SELECT username FROM users WHERE id=%i;"%int(reply["owner"]))[0]["username"]
				editor=db.query("SELECT username FROM users WHERE id=%i;"%int(reply["editor"]))
				if len(editor)==0:
					u413.donttype('<table><tr><td>&gt;</td><td style="text-align:center;width:160px;border-right:solid 1px lime;"><span class="transmit" data-transmit="WHOIS {0}">{0}</span></td><td style="padding-left:8px;padding-right:8px;">{{<span class="transmit" data-transmit="[quote]{1}[/quote]">{1}</span>}}<br/>{2}<br/><br/><span class="dim">Posted {3}</span></td></tr></table><br/>'.format(owner,int(reply["id"]),bbcode.bbcodify(reply["post"]),util.ago(reply["posted"])))
				else:
					editor=editor[0]["username"]
					u413.donttype('<table><tr><td>&gt;</td><td style="text-align:center;width:160px;border-right:solid 1px lime;"><span class="transmit" data-transmit="WHOIS {0}">{0}</span></td><td style="padding-left:8px;padding-right:8px;">{{<span class="transmit" data-transmit="[quote]{1}[/quote]">{1}</span>}}<br/>{2}<br/><br/><i>Edited by <span class="transmit" data-transmit="WHOIS {3}">{3}</span> {4}</i><br/><span class="dim">Posted {5}</span></td></tr></table><br/>'.format(owner,int(reply["id"]),bbcode.bbcodify(reply["post"]),editor,util.ago(reply["edited"]),util.ago(reply["posted"])))
		if c==0:
			u413.donttype('Page 1/1<br/>')
		else:
			u413.donttype('Page %i/%i<br/>'%(page,math.ceil(c/10.0)))
	if page==1:
		u413.set_context("TOPIC %i"%topic)
	else:
		u413.set_context("TOPIC %i %i"%(topic,page))
	u413.clear_screen()

def topic_func(args,u413):
	params=args.split(' ',2)
	if len(params)==0 or not util.isint(params[0]):
		u413.type("Invalid topic ID.")
		return
	topic=int(params[0])
	if len(params)==1:
		page=1
		output_page(topic,1,u413)
	elif len(params)==2:
		if params[1].upper()=="REPLY":
			u413.j["Command"]="REPLY"
			u413.cmddata["topic"]=topic
			u413.continue_cmd()
		else:
			page=1
			if util.isint(params[1]):
				page=int(params[1])
			elif params[1].upper()=='LAST':
				page=int(db.query("SELECT COUNT(*) FROM posts WHERE parent=%i;"%topic)[0]["COUNT(*)"])
				if page==0:
					page=1
				else:
					page=math.ceil(page/10.0)
			output_page(topic,page,u413)
	elif params[1].upper()=="REPLY":
		db.query("INSERT INTO posts (topic,title,parent,owner,editor,post,locked,edited,posted) VALUES(FALSE,'',%i,%i,0,'%s',FALSE,NULL,NOW());"%(topic,u413.user.userid,db.escape(util.htmlify(params[3]))))
		u413.type("Reply made successfully.")

command.Command("TOPIC",'<id> [page | "FIRST" | "LAST" | [REPLY <message>]]',{"id":"The topic ID","page":"The topic page to load (defaults to 1)","message":"The message you wish to post"},"Loads a topic",topic_func,user.User.member)

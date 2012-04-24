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
import bbcode
import re
import util

url=r'((http|ftp|https)://)?([\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&:/~\+#()]*[\w\-\@?^=%&/~\+#()])?)'

bbcodes=[
	r'\[b\](.*?)\[/b\]',
	r'\[i\](.*?)\[/i\]',
	r'\[u\](.*?)\[/u\]',
	r'\[s\](.*?)\[/s\]',
	r'\[url\]%s\[/url\]'%url,
	r'\[img\]%s\[/img\]'%url,
	r'\[url=%s\](.*?)\[/url\]'%url,
	r'\[color=(.*?)\](.*?)\[/color\]',
	r'\[center](.*?)\[/center\]',
	r'\[css=(.*?)\](.*?)\[/css\]'
]

html=[
	r'<b>\1</b>',
	r'<i>\1</i>',
	r'<u>\1</u>',
	r'<del>\1</del>',
	r'<a href="http://\3" target="_blank">\3</a>',
	r'<a href="http://\3" target="_blank">\3</a>',
	r'<a href="http://\3" target="_blank">\6</a>',
	lambda(match):'<span style="color:%s;">%s</span>'%(bbcode.colorify(match.group(1)),match.group(2)),
	r'<center>\1</center>',
	lambda(match):'<span style="%s">%s</span>'%(bbcode.cssify(match.group(1)),match.group(2))
]

def bbcodify(bbcode,exclude=None):
	for x in range(len(bbcodes)):
		bbcode=re.sub(re.compile(bbcodes[x],re.IGNORECASE),html[x],bbcode)
	return bbcode

def wall_func(args,u413):
	r=db.query("SELECT * FROM wall ORDER BY posted;")
	if args.strip()=='':
		if len(r)==0:
			u413.type("There are no notes on the wall.")
		else:
			u413.type("Welcome to the wall!")
			out='<br/><table style="padding-right:8px;">'
			for entry in r:
				u=db.query("SELECT username FROM users WHERE id=%i"%int(entry["user"]))
				out+='<tr><td>{{<span class="transmit" data-transmit="WHOIS {0}">{0}</span>}}</td><td style="padding-left:1em;">{1} <span class="dim">{2}</span></td></tr>'.format(u[0]["username"],bbcodify(entry["text"]),util.ago(entry["posted"]))
			u413.donttype(out+'</table>')
			u413.set_context("WALL")
			u413.clear_screen()
	else:
		if len(r)>=256:
			db.query("DELETE FROM wall ORDER BY posted LIMIT 1;")
		db.query("INSERT INTO wall(user,text) VALUES(%i,'%s');"%(u413.user.userid,db.escape(util.htmlify(args))))
		wall_func('',u413)
		
command.Command("WALL","[note]",{"note":"A note to post to the wall"},"Access/post to the u413 wall.",wall_func,user.User.member)

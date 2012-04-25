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

import re
import database as db
import util
import uuid

url=r'((https?|ftp)://)?([\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#!()]*[\w\-\@?^=%&amp;/~\+#!()])?)'

bbcodes=[
	r'\[b\](.*?)\[/b\]',
	r'\[i\](.*?)\[/i\]',
	r'\[u\](.*?)\[/u\]',
	r'\[s\](.*?)\[/s\]',
	r'\[transmit\](.*?)\[/transmit\]',
	r'\[transmit=(.*?)\](.*?)\[/transmit\]',
	r'\[url=%s\](.*?)\[/url\]'%url,
	r'\[url\]%s\[/url\]'%url,
	r'\[img\]%s\[/img\]'%url,
	r'\[sound\]%s\[/sound\]'%url,
	r'\[audio\]%s\[/audio\]'%url,
	r'\[video\]%s\[/video\]'%url,
	r'\[quote\](\d+)\[/quote\]',
	r'\[quote\](.*?)\[/quote\]',
	r'\[color=(.*?)\](.*?)\[/color\]',
	r'\[center](.*?)\[/center\]',
	r'\[css=(.*?)\](.*?)\[/css\]',
	r'\[br\]',
	r'\[hr\]',
	r'\[tab\]',
	r'\[flash\]%s\[/flash\]'%url,
	r'\[code\](.*?)\[/code\]'
]

def embed_video(match):
	sub=match.group(4)
	site=match.group(3).split('/',1)[0]
	if site=="youtube.com" or site=="www.youtube.com":
		if len(match.groups())>3 and '?' in match.group(3):
			options=match.group(5).split('?',1)
			for option in options:
				parts=option.split('=')
				if parts[0].lower()=='v':
					return '<iframe width="560" height="315" src="http://www.youtube.com/embed/%s" frameborder="0" allowfullscreen></iframe>'%parts[1]
			return '<iframe width="560" height="315" src="http://www.youtube.com/embed/" frameborder="0" allowfullscreen></iframe>'
	elif site=="video.google.com":
		if len(match.groups())>3 and '?' in match.group(5):
			options=match.group(5).split('?',1)
			for option in options:
				parts=option.split('=')
				if parts[0].lower()=='docid':
					return '<iframe width="560" height="315" src="http://video.google.com/googleplayer.swf?docid=%s" frameborder="0" allowfullscreen></iframe>'%parts[1]
		return '<embed style="width:400px; height:326px;" id="VideoPlayback" type="application/x-shockwave-flash" src="http://video.google.com/googleplayer.swf"></embed>'
	elif site=="ebaumsworld.com" or site=="www.ebaumsworld.com":
		if len(match.groups())>3 and "/video/watch/" in match.group(5):
			return '<object type="application/x-shockwave-flash" data="http://www.ebaumsworld.com/player.swf" width="560" height="315" style="visibility: visible;"><param name="allowfullscreen" value="true"><param name="allowScriptAccess" value="always"><param name="wmode" value="opaque"><param name="flashvars" value="id0=%s"></object>'%match.group(5)[len('/video/watch/'):]
		return '<object type="application/x-shockwave-flash" data="http://www.ebaumsworld.com/player.swf" width="560" height="315" style="visibility: visible;"><param name="allowfullscreen" value="true"><param name="allowScriptAccess" value="always"><param name="wmode" value="opaque"></object>'
	u='//'+match.group(1)
	return '<video controls="controls" src="%s">Your browser does not support HTML5.(We recommend <a href="//google.com/chrome">Google Chrome</a>). You can also <a href="%s">download</a> the video instead</video> '%(u,u)

def colorify(s):
	s=s.split(';')[0]+';'
	return s.replace("'","\\'").replace('"','\\"')

def cssify(s):
	return s.replace("'","\\'").replace('"','\\"')

def htmlify(s):
	return s.replace('<','&lt;').replace('>','&gt;').replace('\n','<br/>')

def quote(match):
	post=db.query("SELECT owner,post,posted,parent FROM posts WHERE id=%i;"%int(match.group(1)));
	if len(post)==0:
		return '<div class="quote">%s</div>'%match.group(1)
	post=post[0]
	poster=None
	op=db.query("SELECT id,owner,parent FROM posts WHERE topic=TRUE and id=%i;"%int(post["parent"]))[0]
	if op["parent"]=='4':
		anons=db.query("SELECT DISTINCT owner FROM (SELECT owner,posted FROM posts WHERE parent=%i ORDER BY posted ASC);"%int(op["id"]))
		poster=util.anoncode(anons,int(post["owner"]),int(op["owner"]))
	else:
		poster=db.query("SELECT username FROM users WHERE id=%i;"%int(post["owner"]))[0]["username"]
	return '<div class="quote"><span class="dim">Posted by %s %s</span><br/><br/>%s</div>'%(poster,util.ago(post["posted"]),post["post"])

html=[
	r'<b>\1</b>',
	r'<i>\1</i>',
	r'<u>\1</u>',
	r'<del>\1</del>',
	r'<span class="transmit">\1</span>',
	r'<span class="transmit" data-transmit="\1">\2</span>',
	r'<a href="http://\3" target="_blank">\6</a>',
	r'<a href="http://\3" target="_blank">\3</a>',
	r'<img src="http://\3"/>',
	r'<audio controls="controls" src="http://\3">Your browser does not support HTML5. (We recommend Google Chrome) You can <a href="http://\3">download</a> the audio instead</audio>',
	r'<audio controls="controls" src="http://\3">Your browser does not suport HTML5. (We recommend Google Chrome) You can <a href="http://\3">download</a> the audio instead</audio>',
	embed_video,
	quote,
	r'<br/><div class="quote">\1</div>',
	lambda(match):'<span style="color:%s;">%s</span>'%(colorify(match.group(1)),match.group(2)),
	r'<center>\1</center>',
	lambda(match):'<span style="%s">%s</span>'%(cssify(match.group(1)),match.group(2)),
	r'<br/>',
	r'<hr/>',
	r'<span class="tab"></span>',
	r'<div class="flash"><object classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" width="640" height="390"><param name="movie" value="http://\3"><param name="allowfullscreen" value="true"><param name="allowscriptaccess" value="always"><embed src="http://\3" width="640" height="390" allowscriptaccess="always" allowfullscreen="false"/></object></div>',
	r'<code>\1</code>'
]

for x in range(len(bbcodes)):
	bbcodes[x]=re.compile(bbcodes[x],re.IGNORECASE)

def bbcodify(bbcode,minimal=False):
	bbc=bbcodes
	for x in range(len(bbcodes)):
		while True:
			b=bbcode
			bbcode=re.sub(bbcodes[x],html[x],bbcode)
			if b==bbcode:
				break
	return bbcode

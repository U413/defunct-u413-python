import re

url=r'((http|ftp|https)://)?([\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?)'

bbcodes=[
	r'\[b\](.*)\[/b\]',
	r'\[i\](.*)\[/i\]',
	r'\[u\](.*)\[/u\]',
	r'\[s\](.*)\[/s\]',
	r'\[transmit\](.*)\[/transmit\]',
	r'\[url\]%s\[/url\]'%url,
	r'\[url=%s\](.*)\[/url\]'%url,
	r'\[img\]%s\[/img\]'%url,
	r'\[sound\]%s\[/sound\]'%url,
	r'\[audio\]%s\[/audio\]'%url,
	r'\[video\]%s\[/video\]'%url,
	r'\[quote\](.*)\[/quote\]',
	r'\[color=(.*)\](.*)\[/color\]',
	r'\[center](.*)\[/center\]',
	r'\[css=(.*)\](.*)\[/css\]',
	r'\[br\]',
	r'\[hr\]',
	r'\[tab\]'
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
	u='//'+match.group(1)
	return '<video controls="controls" src="%s">Your browser does not support HTML5.(We recommend <a href="//google.com/chrome">Google Chrome</a>). You can also <a href="%s">download</a> the video instead</video> '%(u,u)

def colorify(s):
	s=s.split(';')[0]+';'
	return s.replace("'","\\'").replace('"','\\"')

def cssify(s):
	return s.replace("'","\\'").replace('"','\\"')

def htmlify(s):
	return s.replace('<','&lt;').replace('>','&gt;').replace('\n','<br/>')

html=[
	r'<b>\1</b>',
	r'<i>\1</i>',
	r'<u>\1</u>',
	r'<del>\1</del>',
	r'<span class="transmit">\1</span>',
	r'<a href="http://\3">\3</a>',
	r'<a href="http://\3">\6</a>',
	r'<img src="//\3"/>',
	r'<audio controls="controls" src="http://\3">Your browser does not suuport HTML5.(We recommend Google Chrome) You can <a href="http://\3">download</a> the audio instead</audio>',
	r'<audio controls="controls" src="http://\3">Your browser does not suuport HTML5.(We recommend Google Chrome) You can <a href="http://\3">download</a> the audio instead</audio>',
	embed_video,
	r'<div class="quote">\1</div>',
	lambda(match):'<span style="color:%s;">%s</span>'%(colorify(match.group(1)),match.group(2)),
	r'<center>\1</center>',
	lambda(match):'<span style="%s">%s</span>'%(cssify(match.group(1)),match.group(2)),
	r'<br/>',
	r'<hr/>',
	r'<span class="tab"></span>'
]

def bbcodify(bbcode):
	for x in range(len(bbcodes)):
		bbcode=re.sub(bbcodes[x],html[x],bbcode)
	return bbcode

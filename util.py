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

import time
import re

def ago(t):
	if type(t)==float:
		t=int(t)
	if type(t)!=int:
		t=int(time.mktime(time.strptime(t,'%Y-%m-%d %H:%M:%S')))
	dif=time.time()-t
	if dif<1:
		return "just now"
	elif dif<60:
		return str(int(dif))+' seconds ago'
	elif dif<60*60:
		if int(dif/60)==1:
			return '1 minute ago'
		else:
			return str(int(dif/60))+' minutes ago'
	elif dif<60*60*24:
		if int(dif/60/60)==1:
			return '1 hour ago'
		else:
			return str(int(dif/60/60))+' hours ago'
	elif dif<60*60*24*7:
		if int(dif/60/60/24)==1:
			return '1 day ago'
		else:
			return str(int(dif/60/60/24))+' days ago'
	elif dif<60*60*24*365:
		if int(dif/60/60/24/7)==1:
			return '1 week ago'
		else:
			return str(int(dif/60/60/24/7))+' weeks ago'
	else:
		if int(dif/60/60/24/365)==1:
			return '1 year ago'
		else:
			return str(int(dif/60/60/24/365))+' years ago'

def until(t):
	if type(t)==float:
		t=int(t)
	if type(t)!=int:
		t=int(time.mktime(time.strptime(t,'%Y-%m-%d %H:%M:%S')))
	dif=t-time.time()
	if dif<1:
		return "in a moment"
	elif dif<60:
		return str(int(dif))+' seconds from now'
	elif dif<60*60:
		if int(dif/60)==1:
			return '1 minute from now'
		else:
			return str(int(dif/60))+' minutes from now'
	elif dif<60*60*24:
		if int(dif/60/60)==1:
			return '1 hour from now'
		else:
			return str(int(dif/60/60))+' hours from now'
	elif dif<60*60*24*7:
		if int(dif/60/60/24)==1:
			return '1 day from now'
		else:
			return str(int(dif/60/60/24))+' days from now'
	elif dif<60*60*24*365:
		if int(dif/60/60/24/7)==1:
			return '1 week ago'
		else:
			return str(int(dif/60/60/24/7))+' weeks from now'
	else:
		if int(dif/60/60/24/365)==1:
			return '1 year from now'
		else:
			return str(int(dif/60/60/24/365))+' years from now'

def isint(i):
	try:
		i=int(i)
	except:
		return False
	return True

def htmlify(s):
	return s.replace('<','&lt;').replace('>','&gt;').replace('\n','<br/>').replace('\t','<span class="tab"></tab>')

def dehtmlify(s):
	return s.replace('&lt;','<').replace('&gt;','>').replace('<br/>','\n').replace('<span class="tab"></tab>','\t')

def stripctrl(i):
	if i:
		# unicode invalid characters
		RE_XML_ILLEGAL=u'([\u0000-\u0008\u000b-\u000c\u000e-\u001f\ufffe-\uffff])'+u'|'+u'([%s-%s][^%s-%s])|([^%s-%s][%s-%s])|([%s-%s]$)|(^[%s-%s])'%(unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff))
		i=re.sub(RE_XML_ILLEGAL,"",i)
		# ascii control characters
		i=re.sub(r"[\x01-\x1F\x7F]","",i)
	return i

def anoncode(anons,owner,op):
	owner=int(owner)
	op=int(op)
	if owner==op:
		return 'OP'
	offset=0
	for i in range(len(anons)):
		if int(anons[i]["owner"])==owner:
			offset=i
			break
	if offset==0:
		return 'A'
	if offset==379:#OP magic number, skip and go to OQ
		offset+=1
	name=''
	while offset>0:
		name+=chr(ord('A')+offset%26)
		offset/=26
	return name

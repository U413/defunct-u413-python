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
			return str(int(dif/60/60/24/365))+' year ago'

def isint(i):
	try:
		i=int(i)
	except:
		return False
	return True

def htmlify(s):
	return s.replace('<','&lt;').replace('>','&gt;').replace('\n','<br/>').replace('\n','<span class="tab"></tab>')

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

import _mysql as mysql

db=mysql.connect("localhost","u413",open("/var/u413.pwd","r").read().rstrip('\r\n'),"u413")

#wrap the ugly _mysql interface with a nice function
#returns a list of dictionaries corresponding to the rows and columns
def query(q):
	db.query(q)
	r=db.store_result()
	if r==None:
		return []
	#format result
	fr=[]
	while True:
		row=r.fetch_row(how=1,maxrows=0)
		if row!=():
			i=0
			while i<len(row):
				fr.append(row[i])
				i=i+1
		else:
			break
	return fr

def escape(data):
	return mysql.escape_string(data)

def count(field,condition):
	return int(query("SELECT COUNT(*) FROM %s WHERE %s;"%(escape(field),condition))[0]["COUNT(*)"])

def anons(topic):
	anons=query("SELECT DISTINCT owner FROM (SELECT owner,posted FROM (SELECT owner,posted FROM posts WHERE topic=FALSE AND parent=%i) AS t1 GROUP BY owner ORDER BY posted) AS t2;"%int(topic))
	for a in range(len(anons)):
		anons[a]=int(anons[a]["owner"])
	return anons

def get_username(uid):
	u=query("SELECT username FROM users WHERE id=%i;"%int(uid))
	if len(u)==0:
		return None
	return u[0]["username"]

def count_posts(topic):
	return count("posts","parent=%i AND topic=FALSE"%int(topic))

def last_post(topic):
	r=query("SELECT owner,posted FROM posts WHERE parent=%i AND topic=FALSE ORDER BY posted DESC LIMIT 1;"%int(topic))
	if len(r)==0:
		return None
	return r[0]

def select_topic(tid):
	r=query("SELECT * FROM posts WHERE topic=TRUE AND id=%i;"%int(tid))
	if len(r)==0:
		return None
	return r[0]

def get_boardname(bid):
	b=query("SELECT name FROM boards WHERE id=%i;"%int(bid))
	if len(b)==0:
		return None
	return b[0]["name"]

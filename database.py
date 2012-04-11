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
	row=(0,)
	while True:
		row=r.fetch_row(how=1,maxrows=0)
		if row!=():
			fr.append(row[0])
		else:
			break
	return fr

def escape(data):
	return mysql.escape_string(data)
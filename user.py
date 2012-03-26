'''u413 - an open-source BBS/terminal/PI-themed forum
	Copyright (C) 2012 PiMaster

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

import cgi
import hashlib
import uuid

import datetime

import database

def sha256(data):
	return hashlib.sha256(data).hexdigest()

class User(object):
	permaban=-10
	banned=-1
	guest=0
	member=10
	halfmod=20
	mod=30
	admin=40
	owner=50
	def __init__(self):
		self.username='Guest'
		self.session=uuid.uuid4()
		self.level=User.guest
		self.userid=0
		self.create_session()
	
	def __init__(self,session):
		r=database.query("SELECT * FROM sessions WHERE id='%s';"%session)
		if len(r)==0:
			self.username='Guest'
			self.session=uuid.uuid4()
			self.level=User.guest
			self.userid=0
			self.create_session()
			return
		r=r[0]
		self.session=session
		self.userid=r["user"]
		if int(self.userid)==0:
			self.username='Guest'
			self.level=User.guest
			return
		else:
			self.username=r["username"]
			self.access=r["access"]
			self.expire=datetime.datetime.strptime(r["expire"],'%Y-%m-%d %H:%M:%S')
			self.context=r["context"]
			self.history=eval(r["history"])
			self.cmd=r["cmd"]
			self.cmddata=r["cmddata"]
	
	def login(self,username,password):
		password=sha256(password)
		r=database.query("SELECT * FROM users WHERE username='%s' AND password='%s';"%(database.escape(username),password))
		if len(r)==0:
			return "Wrong username or password"
		r=r[0]
		self.username=r["username"]
		self.level=r["access"]
		self.userid=r["id"]
		database.query("UPDATE sessions SET username='%s' WHERE id='%s';"%(self.username,self.session))
		database.query("UPDATE sessions SET user='%s' WHERE id='%s';"%(self.userid,self.session))
		database.query("UPDATE sessions SET access='%s' WHERE id='%s';"%(self.level,self.session))
		return "You are now logged in as "+self.username
	
	def logout(self):
		if self.session!="" and self.level!=0:
			database.query("UPDATE sessions SET username='Guest' WHERE id='%s';"%(self.session))
			database.query("UPDATE sessions SET user='0' WHERE id='%s';"%(self.session))
			database.query("UPDATE sessions SET access='0' WHERE id='%s';"%(self.session))
			return "You have been logged out"
		else:
			#TODO: send something to the client that clears cookies
			return "Corrupt login. Cannot logout. Please clear cookies."
		
	def create_session(self):
			database.query("INSERT INTO sessions (id,user,expire,username,access,history,cmd,cmddata) VALUES('%s',%s,NOW(),'%s','%s','','','');"%(self.session,self.userid,self.username,self.level))

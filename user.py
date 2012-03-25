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

import time

import database

def sha256(data):
	return hashlib.sha256(data).hexdigest()

class User(object):
	banned=-1
	guest=0
	member=10
	mod=20
	admin=30
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
			r=database.query("SELECT * FROM users WHERE id='%s';"%self.userid)
			r=r[0]
			self.username=r["username"]
			self.level=r["access"]
	
	def login(self,username,password):
		password=sha256(password)
		r=database.query("SELECT * FROM users WHERE username='%s' AND password='%s';"%(database.escape(username),password))
		if len(r)==0:
			return False
		r=r[0]
		self.username=r["username"]
		self.level=r["access"]
		self.userid=r["id"]
		database.query("UPDATE sessions SET username='%s' WHERE id='%s';"%(self.username))
		database.query("UPDATE sessions SET user='%s' WHERE id='%s';"%(self.userid))
		database.query("UPDATE sessions SET access='%s' WHERE id='%s';"%(self.level))
		return True
	
	def logout(self):
		if self.session!="" and self.level!=0:
			database.query("UPDATE sessions SET username='%s' WHERE id='Guest';")
			database.query("UPDATE sessions SET user='%s' WHERE id='0';")
			database.query("UPDATE sessions SET access='%s' WHERE id='0';")
			return True
		else:
			return False
		
	def create_session(self):
			database.query("INSERT INTO sessions (id,user,expire,username,access,history,cmd,cmddata) VALUES('%s',%s,'%s','%s','%s','','','');"%(self.session,self.userid,time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime()),self.username,self.level))
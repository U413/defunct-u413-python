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

import hashlib
import uuid

import datetime

import database as db

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
	
	def __init__(self,session=None):
		if session==None:
			self.guest_login()
		else:
			r=db.query("SELECT * FROM sessions WHERE id='%s';"%db.escape(session))
			if len(r)==0:
				self.guest_login()
			r=db.query("SELECT * FROM sessions WHERE id='%s';"%db.escape(session))
			if len(r)==0:
				self.username='Guest'
				# if new session is generated then there will never be a cookie match. Thus having disastrous bugs.
				self.session=session #old session is created again ^
				self.level=User.guest
				self.userid=0
				self.level=User.guest
				self.expire=datetime.datetime.today()
				self.context=''
				self.history=[]
				self.cmd=''
				self.cmddata={}
				self.create_session()
				return
			r=r[0]
			self.session=session
			self.userid=r["user"]
			self.name=r["username"]
			self.username=r["username"]
			self.level=r["access"]
			self.expire=datetime.datetime.strptime(r["expire"],'%Y-%m-%d %H:%M:%S')
			self.context=r["context"]
			self.history=eval(r["history"])
			self.cmd=r["cmd"]
			self.cmddata=eval(r["cmddata"])
	
	def guest_login(self):
		self.name='Guest'
		self.session=uuid.uuid4().hex
		self.level=User.guest
		self.userid=0
		self.expire=datetime.datetime.today()
		self.context=''
		self.history=[]
		self.cmd=''
		self.cmddata={}
		self.create_session()
	
	def login(self,username,password):
		password=sha256(password)
		r=db.query("SELECT * FROM users WHERE LCASE(username)='%s' AND password='%s';"%(db.escape(username.lower()),sha256(password)))
		if len(r)==0:
			return "Wrong username or password"
		r=r[0]
		self.name=r["username"]
		self.level=r["access"]
		self.userid=r["id"]
		db.query("UPDATE sessions SET username='%s',user=%i,access=%i WHERE id='%s';"%(self.name,self.userid,self.level,self.session))
		return "You are now logged in as "+self.name
	
	def register(self,username,password,confirmpassword):
		pas=password
		password=sha256(password)
		confirmpassword=sha256(confirmpassword)
		r=db.query("SELECT * FROM users WHERE username='%s';"%username)
		if len(r)!=0 or username.upper()=="PIBOT" or username.upper()=="ADMIN" or username.upper()=="U413" or username.upper()=="MOD" or username.upper()=="QBOT" or username.upper()=="EBOT":
			return "User is in use. Please register with a different username."
		elif password!=confirmpassword:
			return "Password does not match with confirmed password"
		elif self.username!="Guest":
			return "You need to be logged out to register"
		elif len(username)<3:
			return "Size of username has to be atleast 3 characters"
		elif len(password)<3:
			return "Size of password has to be atleast 3 characters"
		else:
			db.query("INSERT INTO users(id,username,password,access) VALUES('','%s','%s','%s');"%(db.escape(username),password,"10"))
			return "Registration successful. "+self.login(username,pas)
	
	def logout(self):
		if self.session!="":
			if self.level!=0:
				return "You're already logged out"
			else:
				db.query("UPDATE sessions SET user=0,username='Guest',access=0,context='',cmd='',cmddata='' WHERE id='%s';"%user.session)
				return "You have been logged out"
		else:
			#TODO: send something to the client that clears cookies
			return "Corrupt login. Cannot logout. Please clear cookies."
		
	def create_session(self):
		db.query("INSERT INTO sessions (id,user,expire,username,access,history,cmd,cmddata) VALUES('%s',%i,DATE_ADD(NOW(),INTERVAL 6 HOUR),'%s',%i,'[]','','{}');"%(self.session,self.userid,self.name,self.level))

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
import time
import datetime
import re

import database as db
import util

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
				return
			r=r[0]
			self.session=session
			self.userid=int(r["user"])
			self.name=r["username"]
			self.level=int(r["access"])
			self.expire=str(r["expire"])
			self.context=r["context"]
			self.history=eval(r["history"])
			self.cmd=r["cmd"]
			self.cmddata=eval(r["cmddata"])
			user=db.query("SELECT muted,alias FROM users WHERE id=%i;"%self.userid)[0]
			self.mute=bool(ord(user["muted"]))
			self.alias=eval(user["alias"])
	
	def guest_login(self):
		self.name='Guest'
		self.session=uuid.uuid4().hex
		self.level=User.guest
		self.userid=1
		self.expire=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()+6*60*60))
		self.context=''
		self.history=[]
		self.cmd=''
		self.cmddata={}
		self.mute=False
		self.alias=[]
		self.create_session()
	
	def login(self,username,password):
		password=sha256(password)
		r=db.query("SELECT * FROM users WHERE LCASE(username)='%s' AND password='%s';"%(db.escape(util.htmlify(username.lower())),password))
		if len(r)==0:
			return False
		r=r[0]
		self.name=r["username"]
		self.level=int(r["access"])
		self.userid=int(r["id"])
		self.mute=bool(ord(r["muted"]))
		db.query("UPDATE sessions SET username='%s',user=%i,access=%i WHERE id='%s';"%(self.name,self.userid,self.level,self.session))
		return True
	
	def logout(self):
		if self.session!="":
			if self.level==0:
				return "You are already logged out."
			else:
				db.query("UPDATE sessions SET user=1,username='Guest',access=0,context='',cmd='',cmddata='' WHERE id='%s';"%self.session)
				return "You have been logged out."
		else:
			#TODO: send something to the client that clears cookies
			return "Corrupt login. Cannot logout. Please clear cookies."
		
	def create_session(self):
		db.query("INSERT INTO sessions (id,user,expire,username,access,history,cmd,cmddata) VALUES('%s',%i,DATE_ADD(NOW(),INTERVAL 6 HOUR),'%s',%i,'[]','','{}');"%(self.session,self.userid,self.name,self.level))

def userlvl(lvl):
	if lvl==User.permaban:
		return "Permabanned"
	elif lvl==User.banned:
		return "Banned"
	elif lvl==User.guest:
		return "Guest"
	elif lvl==User.member:
		return "Member"
	elif lvl==User.halfmod:
		return "Half-Moderator"
	elif lvl==User.mod:
		return "Moderator"
	elif lvl==User.admin:
		return "Admin"
	elif lvl==User.owner:
		return "Owner"
	else:
		return "Unknown"

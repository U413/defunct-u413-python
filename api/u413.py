#!/usr/bin/python
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

from mod_python import Cookie

import json
import os
import sys

def index(req):
	import user
	import command

	cli=req.form.get("cli",None)
	if cli!=None:
		cli=cli.value
	session=req.form.get("session",None)
	if session!=None:
		session=session.value
	#no session
	if session==None:
		jar=Cookie.get_cookies(req)
		if "session" in jar:
			session=jar.get("session",None)
			if session!=None:
				session=session.value
			currentuser=user.User(session)
			if cli==None:
				cli="LOGIN"
		else:
			currentuser=user.User()
			if cli==None:
				cli="INITIALIZE"
	else:
		currentuser=user.User(session)
		if cli==None:
			cli="LOGIN"

	cmdarg=cli.split(' ',1)
	cmd=cmdarg[0]
	args=""
	if len(cmdarg)>1:
		args=cmdarg[1]

	callback=req.form.get("callback",None)

	class u413(object):
		def __init__(self,u):
			self.j={
				"Command":"",
				"ContextText":u.context,
				"CurrentUser":u.name,
				"EditText":None,
				"SessionId":u.session,
				"TerminalTitle":"Terminal - "+u.name,
				"ClearScreen":False,
				"Exit":False,
				"PasswordField":False,
				"ScrollToBottom":True,
				"DisplayItems":[],
				"Notification":None
			}
			self.cmds=command.cmds
			self.user=u
			self.cont=False
			self.cookies=[]
			self.cmddata=u.cmddata
			self.mute=u.mute

		def type(self,text,mute=None):
			if mute==None:
				mute=self.mute
			self.j["DisplayItems"].append({"Text":text,"DontType":False,"Mute":mute})

		def donttype(self,text,mute=None):
			if mute==None:
				mute=self.mute
			self.j["DisplayItems"].append({"Text":text,"DontType":True,"Mute":mute})

		def set_context(self,context):
			self.j["ContextText"]=context
			self.user.context=context

		def set_title(self,title):
			self.j["TerminalTitle"]=title

		def edit_text(self,text):
			self.j["EditText"]=text

		def clear_screen(self):
			self.j["ClearScreen"]=True

		def scroll_down(self):
			self.j["ScrollToBottom"]=True

		def use_password(self):
			self.j["PasswordField"]=True

		def continue_cmd(self):
			self.cont=True
			self.user.cmd=self.j["Command"]

		def set_cookie(self,cookie,value):
			self.cookies.append({"name":cookie,"value":value})

		def exit(self):
			self.j["Exit"]=True
		
		def notify(self,notification):
			self.j["Notification"]=notification
	
		def exec_js(self,start,cleanup=''):
			out=''
			if cleanup!='':
				out+='<div id="mark"></div>'
			out+='<script type="text/javascript">'+start
			if cleanup!='':
				out+='$("#mark").data("cleanup",function(){%s});'%cleanup
			out+='</script>'
			self.donttype(out)

	u=u413(currentuser)

	try:
		import database as db
		import time

		import initialize
		import echo
		import ping
		import login
		import logout
		import register
		import who
		import desu
		import clear
		import boards
		import wall
		import nsfwall
		import history
		import whois
		import users
		import mute
		import alias

		import topic
		import reply
		import newtopic
		import board
		import edit
		import delete
		import move

		import first
		import last
		import prev
		import next
		import refresh

		import help
	
		import messages
		import message
		import newmessage
	
		import sql
	
		import pi
		import pirates
		import b
		import turkey
		import cosmos
		import do
		import rude

		command.respond(cli,u)

		if u.cont:
			u.j["Command"]=currentuser.cmd
			
			if currentuser.cmd!='':
				cmd=currentuser.cmd
			db.query("UPDATE sessions SET expire=DATE_ADD(NOW(),INTERVAL 6 HOUR),cmd='%s',cmddata='%s',context='%s' WHERE id='%s';"%(cmd,db.escape(repr(u.cmddata)),currentuser.context,currentuser.session))
		else:
			db.query("UPDATE sessions SET expire=DATE_ADD(NOW(),INTERVAL 6 HOUR),cmd='',cmddata='{}',context='%s' WHERE id='%s';"%(currentuser.context,currentuser.session))
			
		if callback==None:
			req.content_type='application/json'
		else:
			req.content_type='application/javascript'

		for cookie in u.cookies:
			Cookie.add_cookie(req,Cookie.Cookie(cookie["name"],cookie["value"]))
		session=Cookie.Cookie('session',currentuser.session)
		session.expires=time.time()+6*60*60
		Cookie.add_cookie(req,session)
		
		msgs=int(db.query("SELECT COUNT(*) FROM messages WHERE receiver=%i AND seen=FALSE;"%currentuser.userid)[0]["COUNT(*)"])
		if msgs>0:
			u.notify("You have %i new messages in your inbox."%msgs);

		if callback==None:
			return json.dumps(u.j)
		else:
			return callback+'('+json.dumps(u.j)+')'
	except Exception as e:
		import traceback
		u.donttype('<span class="error">'+traceback.format_exc().replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('\n','<br/>').replace(' '*4,'<span class="tab"></tab>')+'</span>')

		req.content_type="application/json"
		session=Cookie.Cookie('session',currentuser.session)
		session.expires=time.time()+6*60*60
		if callback==None:
			return json.dumps(u.j)
		else:
			return callback+'('+json.dumps(u.j)+')'

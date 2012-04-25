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

import cgi
import cgitb
cgitb.enable(display=1)

import json
import os
import Cookie
import sys

import user
import command

form=cgi.FieldStorage()
cli=form.getvalue("cli")

session=form.getvalue("session")

#no session
if session==None:
	if "HTTP_COOKIE" in os.environ:
		cookie=Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
		if "session" in cookie:
			session=cookie["session"].value
			currentuser=user.User(session)
			if cli==None:
				cli="LOGIN"
		else:
			currentuser=user.User()
			if cli==None:
				cli="INITIALIZE"
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

callback=form.getvalue("callback")

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
			"DisplayItems":[]
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

	import first
	import last
	import prev
	import next
	import refresh

	import help
	
	import pi
	import pirates
	import b
	import turkey
	import cosmos

	command.respond(cli,u)

	day=time.strftime('%A')
	if day=='Thursday' or day=='Friday' or day=='Saturday':
		u.exec_js('if((new Date()).getDay()==5){$("#frame").addClass("capslock");}')

	if u.cont:
		u.j["Command"]=currentuser.cmd

	if callback==None:
		print "Content-type: application/json"
	else:
		print "Content-type: application/javascript"

	for cookie in u.cookies:
		print "Set-Cookie: "+cookie["name"]+"="+cookie["value"]
	print 'Set-Cookie: session='+currentuser.session+'; Max-Age: 21600'

	print

	if callback==None:
		print json.dumps(u.j)
	else:
		print callback+'('+json.dumps(u.j)+')'

	if u.cont:
		if currentuser.cmd!='':
			cmd=currentuser.cmd
		db.query("UPDATE sessions SET expire=DATE_ADD(NOW(),INTERVAL 6 HOUR),cmd='%s',cmddata='%s',context='%s' WHERE id='%s';"%(cmd,db.escape(repr(u.cmddata)),currentuser.context,currentuser.session))
	else:
		db.query("UPDATE sessions SET expire=DATE_ADD(NOW(),INTERVAL 6 HOUR),cmd='',cmddata='{}',context='%s' WHERE id='%s';"%(currentuser.context,currentuser.session))
except Exception as e:
	import traceback
	u.donttype('<span class="error">'+traceback.format_exc().replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('\n','<br/>').replace(' '*4,'<span class="tab"></tab>')+'</span>')

	print "Content-type: application/json"
	print "Set-Cookie: session="+currentuser.session+'; Max-Age: 21600'
	print
	
	if callback==None:
		print json.dumps(u.j)
	else:
		print callback+'('+json.dumps(u.j)+')'

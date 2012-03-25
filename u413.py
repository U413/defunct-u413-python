#!/usr/bin/python
'''u413 - an open-source BBS/terminal/PI-themed forum
	Copyright (C) 2012 PiMaster

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
cgitb.enable(display=1,logdir="/var/www/u413/error")

import json
import os
from os import environ
import Cookie

import user
import command

import initialize
import echo
import ping
import login
import logout
import register
import help

print "Content-type: application/javascript"

form=cgi.FieldStorage()
cli=form.getvalue("cli")

if environ.has_key('HTTP_COOKIE'):
	for cookie in map(str.strip,str.split(environ['HTTP_COOKIE'],';')):
		(key,value )=str.split(cookie,'=');
		if key=="Session":
			currentsession=value
			currentuser=user.User(currentsession)
			if cli==None:
				cli="LOGIN"
			break
	#no session
	else:
		currentuser=user.User('')
		cookie=Cookie.SimpleCookie()
		cookie['Session']=str(currentuser.session)
		print cookie
		if cli==None:
			cli="INITIALIZE"

print "\n\n"
	
cmdarg=cli.split(' ',1)
cmd=cmdarg[0].upper()
arg=""
if len(cmdarg)>1:
	arg=cmdarg[1]

callback=form.getvalue("callback")
if callback==None:
	print json.dumps(command.respond(cmd,arg,currentuser))
else:
	print callback+'('+json.dumps(command.respond(cmd,arg,currentuser))+')'

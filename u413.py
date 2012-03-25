#!/usr/bin/python
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

form=cgi.FieldStorage()
cli=form.getvalue("cli")

if cli==None:
	cli="INITIALIZE"

cmdarg=cli.split(' ',1)
cmd=cmdarg[0].upper()
arg=""
if len(cmdarg)>1:
	arg=cmdarg[1]

print "Content-type: application/javascript"

flag = 0
if environ.has_key('HTTP_COOKIE'):
	for cookie in map(str.strip, str.split(environ['HTTP_COOKIE'], ';')):
		(key, value ) = str.split(cookie, '=');
		if key == "Session":
			currentsession = value
			currentuser = user.User(currentsession)
			flag = 1

if flag == 0:
	currentuser = user.User('')
	cookie = Cookie.SimpleCookie()
	cookie['Session'] = str(currentuser.session)
	print cookie

print "\n\n"

callback=form.getvalue("callback")
if callback==None:
	print json.dumps(command.respond(cmd,arg,currentuser))
else:
	print callback+'('+json.dumps(command.respond(cmd,arg,currentuser))+')'

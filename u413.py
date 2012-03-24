#!/usr/bin/python
import cgi
import cgitb
cgitb.enable(display=0,logdir="/var/www/u413/error")

import json
import os
from os import environ

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
print

flag = 0
if environ.has_key('HTTP_COOKIE'):
	for cookie in map(strip, split(environ['HTTP_COOKIE'], ';')):
		(key, value ) = split(cookie, '=');
		if key == "UID":
			currentsession = value
			currentuser = user.User(currentsession)
			flag = 1

if flag == 0:
	currentuser = user.User()
	print "Set-Cookie:UID="+currentuser.session+";\n"
	print "Set-Cookie:Domain=www.u413.com;\n"
	print "Set-Cookie:Path=/;\n"

callback=form.getvalue("callback")
if callback==None:
	print json.dumps(command.respond(cmd,arg,currentuser))
else:
	print callback+'('+json.dumps(command.respond(cmd,arg,currentuser))+')'

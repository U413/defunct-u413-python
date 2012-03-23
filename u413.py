#!/usr/bin/python
import cgi
import cgitb
cgitb.enable(display=0,logdir="/var/www/u413/error")

import json
import os

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

callback=form.getvalue("callback")
if callback==None:
	print json.dumps(command.respond(cmd,arg,None))
else:
	print callback+'('+json.dumps(command.respond(cmd,arg,None))+')'

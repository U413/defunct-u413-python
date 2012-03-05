#!/usr/bin/env python
import cgi
import cgitb
cgitb.enable(display=0,logdir="/var/www/u413/error")

import json
import os

def header(status=200):
	if status!=200:
		print "Status:",status
	print "Content-type: application/javascript"
	print

def output(data):
	callback=form.getvalue("callback")
	if callback==None:
		print json.dumps(data)
	else:
		print callback+'('+json.dumps(data)+')'

#default JSON
djson={
	"Command":"",
	"ContextText":"",
	"CurrentUser":None,
	"EditText":None,
	"SessionId":None,
	"TerminalTitle":"Terminal - Visitor",
	"ClearScreen":False,
	"Exit":False,
	"PasswordField":False,
	"ScrollToBottom":True,
	"DisplayItems":[]
}

form=cgi.FieldStorage()
cli=form.getvalue("cli")

if cli==None:
	cli="INITIALIZE"

cmdarg=cli.split(' ',1)
cmd=cmdarg[0].upper()
arg=""
if len(cmdarg)>1:
	arg=cmdarg[1]

if cmd=="INITIALIZE":
	logo=open("logo.txt","r").read()
	tmp=djson.copy()
	tmp.update({
		"DisplayItems":[
			{
				"Text":"Welcome to...",
				"Mute":False,
				"DontType":False
			},{
			
				"Text":logo,
				"Mute":False,
				"DontType":True
			},{
				"Text":'<span style="color:#f00;">U413 is currently down for maintenance and is expected to be up by March 25.</span>',
				"Mute":False,
				"DontType":True
			}
		],
		"Command":"INITIALIZE",
		"ClearScreen":True
	})
	header()
	output(tmp)
elif cmd=="ECHO":
	tmp=djson.copy()
	tmp.update({
		"DisplayItems":[{
			"Text":arg,
			"Mute":False,
			"DontType":False
		}],
		"Command":"ECHO"
	})
	header()
	output(tmp)
else:
	tmp=djson.copy()
	tmp.update({"DisplayItems":[
		{
			"Text":'<span class="error">"%s" is not a command.</span>'%cmd,
			"Mute":False,
			"DontType":True
		}
	]})
	header()
	output(tmp)

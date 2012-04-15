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

import database as db
import command
import user

def is_stupid(u,p):
	if len(p)<=4:
		return True
	p=p.lower()
	u=u.lower()
	#relation to username
	if u==p or u==p[::-1]:
		return True
	#most used passwords
	bad=[
		"password",
		"qwerty",
		"abc123",
		"monkey",
		"letmein",
		"trustno1",
		"dragon",
		"baseball",
		"iloveyou",
		"master",
		"sunshine",
		"ashley",
		"bailey",
		"passw0rd",
		"shadow",
		"superman",
		"qazwsx",
		"michael",
		"football"
	]
	if p in bad:
		return True
	#go after stuff like abcdefg or 12345678
	count=0
	last=p[0]
	for c in p:
		if ord(c)==ord(last)+1 or ord(c)==ord(last)-1:
			count+=1
		last=c
	if count>=len(p)/2:
		return True
	#alright, you're not stupid
	return False
	
def is_taken(u):
	r=db.query("SELECT * FROM users WHERE LCASE(username)='%s';"%db.escape(u.lower()))
	return len(r)!=0

#REGISTER [username] [password] [confirmation]
#REGISTER
#(1)USERNAME>
#(2)PASSWORD>
#(3)CONFIRM PASSWORD>
#or
#REGISTER username
#(2)PASSWORD>
#(3)CONFIRM PASSWORD>
#or
#REGISTER username password
#(3)CONFIRM PASSWORD>
def register_func(args,u413):
	#check for special cases
	if u413.user.name!="Guest":
		u413.type("You need to be logged out to register.")
		return
	params=args.split()
	#REGISTER has already requested continuation
	if "step" in u413.cmddata:
		if args=="":
			u413.type("Action cancelled.")
			u413.set_context("")
			return
		#Note: For all, ignore extra arguments
		#USERNAME>
		if u413.cmddata["step"]==1:
			if is_taken(params[0]):
				u413.type("Username already in use.")
			else:
				u413.cmddata["username"]=params[0]
				u413.cmddata["step"]=2
				u413.type("Enter a password:")
				u413.set_context("PASSWORD")
				u413.continue_cmd()
				u413.use_password()
		#PASSWORD>
		elif u413.cmddata["step"]==2:
			if is_stupid(u413.cmddata["username"],params[0]):
				u413.type("That's a stupid password. Pick another one.")
			else:
				u413.cmddata["password"]=params[0]
				u413.cmddata["step"]=3
				u413.type("Confirm your password:")
				u413.set_context("CONFIRM PASSWORD")
			u413.continue_cmd()
			u413.use_password()
		#CONFIRM PASSWORD>
		elif u413.cmddata["step"]==3:
			if u413.cmddata["password"]==params[0]:
				db.query("INSERT INTO users(username,password,access) VALUES('%s','%s',%i);"%(db.escape(u413.cmddata["username"]),user.sha256(params[0]),user.User.member))
				u413.type("You are now registered.")
			else:
				u413.type("Passwords do not match.")
	#initial use of command
	else:
		#REGISTER
		if len(args)==0:
			u413.cmddata["step"]=1
			u413.type("Enter your desired username:")
			u413.set_context("USERNAME")
			u413.continue_cmd()
		#REGISTER username
		elif len(args)==1:
			if is_taken(params[0]):
				u413.type("Username already in use.")
			else:
				u413.cmddata["username"]=params[0]
				u413.cmddata["step"]=2
				u413.type("Enter a password:")
				u413.set_context("PASSWORD")
				u413.continue_cmd()
		#REGISTER username password
		#Note: ignore anything after username/password
		else:
			if is_taken(params[0]):
				u413.type("Username already in use.")
			elif is_stupid(params[1]):
				u413.cmddata["username"]=params[0]
				u413.cmddata["step"]=2
				u413.type("That's a stupid password. Pick another one.")
				u413.continue_cmd()
				u413.use_password()
			else:
				u413.cmddata["username"]=params[0]
				u413.cmddata["password"]=params[1]
				u413.cmddata["step"]=3
				u413.type("Confirm your password:")
				u413.set_context("CONFIRM PASSWORD")
				u413.continue_cmd()
				u413.use_password()
	
command.Command("REGISTER","Allows the user to create an account in U413.",register_func,0)

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

import command
import database as db
import user

def login_func(args,u413):
	#check for special cases
	if u413.user.name!="Guest":
		u413.type("You are logged in as "+u413.user.name+'.')
		return
	params=args.split(' ')
	#LOGIN already requested continuation
	if "step" in u413.cmddata:
		if args=="":
			u413.set_context("")
			u413.type("Action cancelled.")
		#USERNAME>
		if u413.cmddata["step"]==1:
			u413.cmddata["username"]=params[0]
			u413.cmddata["step"]=2
			u413.type("Enter your username:")
			u413.set_context("PASSWORD")
			u413.use_password()
			u413.continue_cmd()
		#PASSWORD>
		elif u413.cmddata["step"]==2:
			if u413.user.login(u413.cmddata["username"],params[0]):
				u413.type("You are now logged in as "+u413.user.name+'.')
			else:
				u413.type("Invalid username/password.")
		#else left out because it's impossible
	#First use of LOGIN
	else:
		#LOGIN
		if len(args)==0:
			u413.cmddata["step"]=1
			u413.type("Enter your username:")
			u413.set_context("USERNAME")
			u413.continue_cmd()
		#LOGIN username
		elif len(params)==1:
			u413.cmddata["step"]=2
			u413.cmddata["username"]=params[0]
			u413.type("Enter your password:")
			u413.set_context("PASSWORD")
			u413.use_password()
			u413.continue_cmd()
		#LOGIN username password [ignored args]
		else:
			if u413.user.login(params[0],params[1]):
				u413.type("You are now logged in as "+u413.user.name+'.')
			else:
				u413.type("Invalid username/password.")

command.Command("LOGIN","Logs a user onto U413",login_func,0)

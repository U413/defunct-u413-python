'''u413 - an open-source BBS/terminal/PI-themed forum
	Copyright (C) 2012 PiMaster

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
import display
import database

def login_func(args,user):
	params=args.split(" ")
	out=command.Command.json.copy()
	if args=="" and user.username=="Guest" and user.context=="":
		user.context="USERNAME"
		out.update({
			"DisplayItems":[display.Item("Enter Your Username :")],
			"ContextText":user.context
		})
		database.query("UPDATE sessions SET context='%s' WHERE id='%s';"%(user.context,user.session))
	elif user.username=="Guest" and user.context=="USERNAME":
		user.context="PASSWORD"
		user.cmddata={'STEP1':args}
		out.update({
			"DisplayItems":[display.Item("Enter Your Password :")],
			"ContextText":user.context,
			"PasswordField":True
		})
		database.query("UPDATE sessions SET context='%s',cmddata='%s' WHERE id='%s';"%(user.context,database.escape(str(user.cmddata)),user.session))
	elif user.username=="Guest" and user.context=="PASSWORD":
		user.context=""
		out.update({
			"DisplayItems":[display.Item(user.login(user.cmddata['STEP1'],args))]
		})
		database.query("UPDATE sessions SET context='',cmddata='{}' WHERE id='%s';"%(user.session))
	elif len(params)==2:
		out.update({
			"DisplayItems":[display.Item(user.login(params[0],params[1]))]
		})
	elif args=="" and user.username!="Guest":
		out.update({
			"DisplayItems":[display.Item("You are logged in as "+user.username)]
		})
	else:
		out.update({
			"DisplayItems":[display.Item("Invalid Parameters")]
		})
	return out

command.Command("LOGIN","Logs a user onto U413",login_func,0)

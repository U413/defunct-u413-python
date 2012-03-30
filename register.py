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

import database
import command
import display
import user as us

def register_func(args,user):
	out=command.Command.json.copy()
	params=args.split(" ")
	if args=="" and user.username=="Guest" and user.context=="":
		user.context="USERNAME"
		out.update({
			"DisplayItems":[display.Item("Enter Desired Username :")],
			"ContextText":user.context
		})
		database.query("UPDATE sessions SET context='%s' WHERE id='%s';"%(user.context,user.session))
	elif user.username=="Guest" and user.context=="USERNAME":
		user.context="PASSWORD"
		user.cmddata={'STEP1':args}
		out.update({
			"DisplayItems":[display.Item("Enter Desired Password :")],
			"ContextText":user.context,
			"PasswordField":True
		})
		database.query("UPDATE sessions SET context='%s',cmddata='%s' WHERE id='%s';"%(user.context,database.escape(str(user.cmddata)),user.session))
	elif user.username=="Guest" and user.context=="PASSWORD":
		user.context="CONFIRM PASSWORD"
		user.cmddata['STEP2']=args
		out.update({
			"DisplayItems":[display.Item("Please Confirm Password :")],
			"ContextText":user.context,
			"PasswordField":True
		})
		database.query("UPDATE sessions SET context='%s',cmddata='%s' WHERE id='%s';"%(user.context,database.escape(str(user.cmddata)),user.session))
	elif user.username=="Guest" and user.context=="CONFIRM PASSWORD":
		user.context=""
		out.update({
			"DisplayItems":[display.Item(user.register(user.cmddata['STEP1'],user.cmddata['STEP2'],args))]
		})
		database.query("UPDATE sessions SET context='',cmddata='{}' WHERE id='%s';"%(user.session))
	elif len(params)==3:
		out.update({
			"DisplayItems":[display.Item(user.register(params[0],params[1],params[2]))]
		})
	elif args=="" and user.username!="Guest":
		out.update({
			"DisplayItems":[display.Item("You need to be logged out to register")]
		})
	else:
		out.update({
			"DisplayItems":[display.Item("Invalid Parameters")]
		})
	return out
	
command.Command("REGISTER","Allows the user to creat an account in U413.",register_func,0)
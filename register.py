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
	args=args.split(" ")
	if len(args)==3:
		r=database.query("SELECT * FROM users WHERE username='%s';"%args[0])
		if len(r)!=0 or args[0].upper=="PIBOT" or args[0].upper=="ADMIN" or args[0].upper=="U413" or args[0].upper=="MOD" or args[0].upper=="QBOT" or args[0].upper=="EBOT":
			out.update({
				"DisplayItems":[display.Item("User is in use. Please register with a different username.")]
			})
		elif args[1]!=args[2]:
			out.update({
				"DisplayItems":[display.Item("Password does not match with confirmed password")]
			})
		elif user.username!="Guest":
			out.update({
				"DisplayItems":[display.Item("You need to be logged out to register")]
			})
		elif len(args[0])<3:
			out.update({
				"DisplayItems":[display.Item("Size of username has to be atleast 3 characters")]
			})
		elif len(args[1])<3:
			out.update({
				"DisplayItems":[display.Item("Size of password has to be atleast 3 characters")]
			})
		else:
			database.query("INSERT INTO users(id,username,password,access) VALUES('','%s','%s','%s');"%(database.escape(args[0]),us.sha256(args[1]),"10"))
			out.update({
				"DisplayItems":[display.Item("Registration successful. "+user.login(args[0],args[1]))]
			})
	else:
		out.update({
			"DisplayItems":[display.Item("Invalid Parameters")]
		})
	return out
	
command.Command("REGISTER","Allows the user to creat an account in U413.",register_func,0)
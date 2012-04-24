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
import user

def turkey_func(args,u413):
	u413.donttype('<center><iframe width="560" height="315" src="http://youtube.com/v/ZBJFmRKjCq4&autoplay=1" frameborder="0" allowfullscreen></iframe></center>')
	u413.clear_screen()

command.Command("turkey","",{},"View the magnificance of turkey.",turkey_func,user.User.guest,True)

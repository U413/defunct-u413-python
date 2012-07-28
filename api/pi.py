'''u413 - an open-source BBS/terminal/PI-themed forum
	Copyright (C) 2012 PiMaster
	Copyright (C) 2012 EnKrypt

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU Affero General Public License as published by
	the Free Software Foundation,either version 3 of the License,or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU Affero General Public License for more details.

	You should have received a copy of the GNU Affero General Public License
	along with this program.  If not,see <http://www.gnu.org/licenses/>.'''

import command
import user

def pi_func(args,u413):
	u413.donttype('<center><img src="content/pi.png"/><audio id="pi" src="content/sounds/pi.ogg" autoplay="autoplay"></audio></center>')
	u413.clear_screen()

command.Command("PI","",{},"PI in its magnificence.",pi_func,user.User.guest,True)
command.Command("3.14","",{},"PI in its magnificence.",pi_func,user.User.guest,True)

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

def desu_func(args,u413):
	if "desucount" not in u413.cmddata:
		u413.cmddata["desucount"]=1
	elif u413.cmddata["desucount"]<256:
		u413.cmddata["desucount"]*=2
	u413.donttype(("DESU "*u413.cmddata["desucount"])[:-1])
	u413.set_context("DESU")
	u413.continue_cmd()

command.Command("DESU","[anything]",{"anything":"Type anything and the DESU will continue"},"Keep typing 'DESU'. Maybe if you type it enough, you will turn Japanese.",desu_func,0,True)

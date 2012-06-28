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

def do_func(args,u413):
	if args.upper()=="A BARREL ROLL":
		u413.donttype("<style>.barrel_roll {"+
		"-webkit-transition: -webkit-transform 4s ease;"+
		"-webkit-transform: rotate(360deg);"+
		"-moz-transition: -moz-transform 4s ease;"+
		"-moz-transform: rotate(360deg);"+
		"-o-transition: -o-transform 4s ease;"+
		"-o-transform: rotate(360deg);"+
		"transition: transform 4s ease;"+
		"transform: rotate(360deg);"+
		"} " +
		"</style>"+
		"<script>"+
		"$('body').addClass('barrel_roll');"+
		"setTimeout(function() { $('body').removeClass('barrel_roll'); }, 4000);"+
		"</script>")
	else:
		u413.type("Action not in do action list")

command.Command("DO","[action]",{"action":"Will perform the action if it is valid - such as DO A BARREL ROLL"},"Performs an action if it is the action list.",do_func,0)

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

logo=''' &nbsp;__ &nbsp;__ &nbsp;__ __ &nbsp; &nbsp; &nbsp; _ &nbsp; &nbsp; __<br/> /\ \/\ \/\ \\ \ &nbsp; &nbsp;/&#39; \ &nbsp;/&#39;__`\<br/> \ \ \ \ \ \ \\ \ &nbsp;/\_, \/\_\L\ \<br/> &nbsp;\ \ \ \ \ \ \\ \_\/_/\ \/_/_\_&lt;_<br/> &nbsp; \ \ \_\ \ \__ ,__\ \ \ \/\ \L\ \<br/> &nbsp; &nbsp;\ \_____\/_/\_\_/ &nbsp;\ \_\ \____/<br/> &nbsp; &nbsp; \/_____/ &nbsp;\/_/ &nbsp; &nbsp; \/_/\/___/<br/><br/>'''

def init_func(args,u413):
	u413.type("Welcome to...")
	u413.donttype(logo)
	u413.donttype('<span style="color:#f00;">Coming soon to a browser near you!</span>')
	u413.clear_screen()

command.Command("INITIALIZE","Initialize the terminal.",init_func,0)

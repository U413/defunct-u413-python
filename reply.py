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

'''
+--------+--------------+------+-----+---------+----------------+
| Field  | Type         | Null | Key | Default | Extra          |
+--------+--------------+------+-----+---------+----------------+
| id     | int(11)      | NO   | PRI | NULL    | auto_increment |
| topic  | bit(1)       | YES  |     | NULL    |                |
| title  | varchar(128) | YES  |     | NULL    |                |
| parent | int(11)      | YES  |     | NULL    |                |
| owner  | int(11)      | YES  |     | NULL    |                |
| editor | int(11)      | YES  |     | NULL    |                |
| post   | text         | YES  |     | NULL    |                |
| locked | bit(1)       | YES  |     | NULL    |                |
| edited | datetime     | YES  |     | NULL    |                |
| posted | datetime     | YES  |     | NULL    |                |
+--------+--------------+------+-----+---------+----------------+
'''

import command
import user
import database as db
import topic as modtopic

def reply_func(args,u413):
	#already used REPLY
	if "topic" in u413.cmddata:
		if args.strip()=='':
			u413.type("Action cancelled.")
		else:
			topic=u413.cmddata["topic"]
			db.query("INSERT INTO posts (topic,title,parent,owner,editor,post,locked,edited,posted) VALUES(FALSE,'',%i,%i,0,'%s',FALSE,NULL,NOW());"%(topic,u413.user.userid,db.escape(args)))
			modtopic.topic_func('%i'%topic,u413)
	#first use of REPLY
	else:
		#REPLY
		if args.strip()=='':
			if "TOPIC" in u413.user.context:
				u413.cmddata["topic"]=int(u413.user.context.split(' ')[1])
				u413.type("Enter your reply:")
				u413.set_context("REPLY")
				u413.continue_cmd()
			else:
				u413.donttype('<span class="error">"REPLY" is not a valid command or is not available in the current context.</span>')
		#REPLY [message]
		else:
			if "TOPIC" in u413.user.context:
				topic=int(u413.user.context.split(' ')[1])
				db.query("INSERT INTO posts (topic,title,parent,owner,editor,post,locked,edited,posted) VALUES(FALSE,'',%i,%i,0,'%s',FALSE,NULL,NOW());"%(topic,u413.user.userid,db.escape(args)))
				modtopic.topic_func('%i'%topic,u413)
			else:
				u413.donttype('<span class="error">"REPLY" is not a valid command or is not available in the current context.</span>')

command.Command("REPLY","[message]",{"message":"The message you wish to post"},"Replies to a topic.",reply_func,user.User.member)

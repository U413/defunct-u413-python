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
import util

import topic as modtopic

def reload_topic(t,p,u413):
	modtopic.output_page(t,p,u413)

def reply_func(args,u413):
	#already used REPLY
	if "step" in u413.cmddata:
		if args.strip()=='':
			u413.type("Action cancelled.")
			u413.set_context("")
		#ID>
		elif u413.cmddata["step"]==1:
			if util.isint(args):
				u413.cmddata["step"]=2
				u413.cmddata["topic"]=int(args)
				u413.type("Enter your reply:")
				u413.set_context("REPLY")
				u413.continue_cmd()
			else:
				u413.type("Invalid topic ID.")
				u413.set_context("")
		#REPLY>
		elif u413.cmddata["step"]==2:
			db.query("INSERT INTO posts (topic,title,parent,owner,editor,post,locked,edited,posted) VALUES(FALSE,'',%i,%i,0,'%s',FALSE,NULL,NOW());"%(u413.cmddata["topic"],u413.user.userid,db.escape(args)))
			reload_topic(u413.cmddata["topic"],u413.cmddata["page"],u413)
	#first use of REPLY
	else:
		params=args.split(' ',1)
		context=u413.user.context.split(' ')
		#REPLY
		if args.strip()=='':
			if "TOPIC" in u413.user.context:
				u413.cmddata["step"]=2
				u413.cmddata["topic"]=int(u413.user.context.split(' ')[1])
				u413.type("Enter your reply:")
				u413.set_context("REPLY")
				u413.continue_cmd()
			else:
				u413.cmddata["step"]=1
				u413.type("Enter the topic ID:")
				u413.set_context("TOPIC ID")
				u413.continue_cmd()
		#REPLY [id]
		elif len(params)==1:
			if util.isint(params[0]):
				u413.cmddata["step"]=2
				u413.cmddata["topic"]=int(params[0])
				u413.type("Enter your reply:")
				u413.continue_cmd()
			elif "TOPIC" in u413.user.context:
				topic=int(u413.user.context.split(' ')[1])
				db.query("INSERT INTO posts (topic,title,parent,owner,editor,post,locked,edited,posted) VALUES(FALSE,'',%i,%i,0,'%s',FALSE,NULL,NOW());"%(topic,u413.user.userid,db.escape(args)))
				page=1
				if len(context)>2:
					page=int(context[2])
				reload_topic(int(context[1]),page,u413)
			else:
				u413.type("Invalid topic ID.")
		#REPLY [[id] message]
		else:
			if util.isint(params[0]):
				if len(params)==2:
					db.query("INSERT INTO posts (topic,title,parent,owner,editor,post,locked,edited,posted) VALUES(FALSE,'',%i,%i,0,'%s',FALSE,NULL,NOW());"%(int(params[0]),u413.user.userid,db.escape(params[1])))
					page=1
					if len(context)>2:
						page=int(context[2])
					u413.type("Reply added successfully.")
				else:
					u413.cmddata["step"]=2
					u413.cmddata["topic"]=int(params[0])
					u413.type("Enter your reply:")
					u413.set_context("REPLY")
					u413.continue_cmd()
			elif "TOPIC" in u413.user.context:
				topic=int(u413.user.context.split(' ')[1])
				db.query("INSERT INTO posts (topic,title,parent,owner,editor,post,locked,edited,posted) VALUES(FALSE,'',%i,%i,0,'%s',FALSE,NULL,NOW());"%(topic,u413.user.userid,db.escape(args)))
				page=1
				if len(context)>2:
					page=int(context[2])
				reload_topic(topic,page,u413)
			else:
				u413.type("Topic ID required.")
		u413.cmddata["page"]=1
		if len(context)>2:
			u413.cmddata["page"]=int(context[2])

command.Command("REPLY","[[id] message]",{"id":"The topic ID to reply to","message":"The message you wish to post"},"Replies to a topic.",reply_func,user.User.member)

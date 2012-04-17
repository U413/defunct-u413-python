u413 - an open-source BBS/terminal/PI-themed forum
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
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

Boards:
	1/0 -- Paradox*
	i -- Imaginary* ?
	-1 -- Negative*
	0 -- All
	1 -- Links
	2 -- Site
	3 -- Programming
	4 -- Anon
	5 -- Video/movies
	6 -- Audio/music
	7 -- Games
	8 -- Literature
	9 -- Math
	10 -- Science/skepticism
	11 -- Foreign
	12 -- Misc
	13 -- Test
	20 -- Brony (20% cooler)*
	33 -- Religion/spiritualism
	37 -- Comic (first xkcd comic with "My hobby")*
	42 -- Life the Universe and Everything*
	69 -- NSFW (special behavior - doesn't show up in board 0)
	117 -- Halo (Master Chief's number)*
	151 -- Anime (151 original pokemon)*
	271 -- E*
	314 -- Pi*
	403 -- Access Denied (possible special behavior - return "Acess denied" for all users)*
	404 -- Error*
	413 -- Mod (special behavior - only visible to mods/admins)
	420 -- Get high*
	511 -- Anonymous (5th of November)*
	628 -- Tau*
	666 -- Hell*
	911 -- Emergency*
	1337 -- 1337*
	9001 -- OVER NINE THOUSAND (meme board)*
	12345 -- Gambling*
	122112 -- End of the World*
*=hidden

-= Easter Egg Commands =-
	DO A BARREL ROLL - do what Google does
	TILT - tilt u413
	^^VV<><>BABA - Matrix (or something else cool)
	3.14 or PI - Pi symbol and song
	PIRATES - We are pirates song
	NYAN - u413 becomes colorful (rainbows) and the nyan cat song plays
	PLAY HIM OFF - Play him off keyboard cat video appears
	TURKEY - Gym Battle Vs Turkey video appears
	NEIN - Hitler NEIN video appears
	FUCK YOU - Auto ban for a day
	RUDE - Prints "NOU"
	BUCKET - Shows a video of Karkat freaking out because buckets
	GOT TIGER - Shows a picture of "Got Tiger" (Homestuck)
	WH4T NOW? - Shows Terezi dancing with "WH4T NOW"
	/B/ - Trololol video
	LAIONI - All posts become horrifically misspelled with tons of typos
	HOMESTUCK - Displays video of [S] Cascade and "[url=mspaintadventures.com/?s=6]Homestuck[/url]"
	LET IT SNOW - Makes it snow
	KILL IT WITH FIRE - Make fire burn the page
	BADGERS - MrWeebl's "Badgers"

-= Global Commands =-
	CANCEL - Cancels the current action.
	CLS - Clears the screen.
	HELP [Command] - Displays the help menu.

-= User Commands =-
	ALIAS <Shortcut/DELETE> <Value/Shortcut> - Allows you to specify a terminal shortcut command.
	BOARD <ID/ALL> [Page#/NEWTOPIC] [/TITLE <Title>] [/BODY <Body>] - Displays a list of topics associated with the specified discussion board.
	BOARDS - Displays a list of board categories.
	CHANGEPASSWORD [Password] [Confirm Password] - Update your password.
	LOGOUT - Logs out the current authenticated user.
	MESSAGE <Message ID> [REPLY/DELETE] - Read a message.
	MESSAGES [SENT] - View your messages.
	MUTE <ON/OFF> - Mutes/Unmutes the terminal.
	NEWMESSAGE [/SUBJECT <Subject>] [Username] [/BODY <Body>] - Allows you to send a private message to another user.
	SETTIMEZONE [ID] - Updates your time zone.
	TOPIC <ID> [Page#/REPLY/EDIT/DELETE [Reply ID]] - Displays a topic and its replies.
	USERS - Displays a list of online users.
	INITIALIZE - Prints the introduction to u413 (Only works before login) *

-= Page Shortcut Commands =-
	REFRESH - Reload the current page.
	NEXT - Increase the current page by one.
	PREV - Decrease the current page by one.
	FIRST - Change current page to the first page.
	LAST - Change current page to the last page.

-= Formatting Tags =-
	[b]text[/b] - Bolds the surrounded text.
	[i]text[/i] - Italicizes the surrounded text.
	[u]text[/u] - Underlines the surrounded text.
	[s]text[/s] - Strikes through the surrounded text.
	[img]image url[/img] - Inserts an image.
	[code(=language)]text[/code] - Formats the surrounded text to preserve indentation and highlight syntax (NOTE: Figure out a way to auto-detect languages).
	[quote]text[/quote] - Formats the surrounded text to denote a quote by another user.
	[quote]REPLY ID[/quote] - Quotes the specified reply.
	[url=URL]URL or text[/url] - Formats text to link to the URL or links to the URL. *
	*[transmit]text[/transmit] - Formats the text so that clicking it puts it in the prompt. *
	[color=HEX]text[/color] - Formats the text so that it's in color (Note: Only hex values are supported) *
	SHIFT + ENTER - Drop down a line in forum posts.
	
	[video]link[/video] - Displays a video (video formats, NOT FOR YOUTUBE) (NOTE: figure out a way to make this like u413.tv).
	[youtube]link/id[/video] - Displays a youtube video (NOTE: May be deprecated in the future).
	[audio]link[/audio] - Plays audio (with controls - no autoplay).
	*[flash]link[/flash] - Embeds a flash animation/game.
	*[js]code[/js] - Embeds javascript in an iframe.
	[css=code]text[/css] - Styles text.
	*[spoiler(=label)]text[/spoiler] - Hides text under a label until the user clicks a button.
	*[list=start (ex: a A 1, none means unordered)][*]item 1 [*]item 2 [*] item 3 [/list] - Make an ordered or unordered list.
	*[table][row][column]stuff[/column][/row][/table] - Build a table.

* = not yet implemented

Requests sent to u413 should be JSON using the following format:
{
	parseAsHtml:true,
	cli:"HELP"
}

Responses returned by u413 are JSON with the following format:
{
	Command:"HELP",
	ContextText:"BOARD 3",
	CurrentUser:"",
	EditText:"This is text that goes into the CLI",
	SessionId:"The session ID (usually something like jJJ98s3jd90Jj45ovjsjv6JDc)",
	TerminalTitle:"Terminal - Visitor",
	ClearScreen:false,
	Exit:false,
	Error:false,
	PasswordField:false,
	ScrollToBottom:true,
	DisplayItems:
	[
		{
			Text:"",
			DontType:false,
			Mute:true
		},
		{...}
	]
}

Database organization:

database u413
	table boards
		+--------+-------------+------+-----+---------+-------+-------------------+
		| Field  | Type        | Null | Key | Default | Extra |    Description    |
		+--------+-------------+------+-----+---------+-------+-------------------+
		| id     | int(11)     | NO   | PRI | NULL    |       |  id of the board  |
		| name   | varchar(32) | YES  |     | NULL    |       | name of the board |
		| onall  | bit(1)      | YES  |     | NULL    |       | displayed on all? |
		| hidden | bit(1)      | YES  |     | NULL    |       | hidden on boards? |
		+--------+-------------+------+-----+---------+-------+-------------------+
	
	table posts (topics and replies)
		+--------+--------------+------+-----+---------+----------------+----------------------+
		| Field  | Type         | Null | Key | Default | Extra          |     Description      |
		+--------+--------------+------+-----+---------+----------------+----------------------+
		| id     | int(11)      | NO   | PRI | NULL    | auto_increment |    id of the post    |
		| topic  | bit(1)       | YES  |     | NULL    |                |    is it a topic?    |
		| title  | varchar(128) | YES  |     | NULL    |                |    title (topics)    |
		| parent | int(11)      | YES  |     | NULL    |                | parent (board/topic) |
		| owner  | int(11)      | YES  |     | NULL    |                |    owner of post     |
		| editor | int(11)      | YES  |     | NULL    |                |    editor of post    |
		| post   | text         | YES  |     | NULL    |                |  the post's content  |
		| locked | bit(1)       | YES  |     | NULL    |                |    topic locked?     |
		| edited | datetime     | YES  |     | NULL    |                |   time of editing    |
		| posted | datetime     | YES  |     | NULL    |                |   time of posting    |
		+--------+--------------+------+-----+---------+----------------+----------------------+
	
	table sessions
		+----------+-------------+------+-----+---------+-------+--------------------+
		| Field    | Type        | Null | Key | Default | Extra |    Description     |
		+----------+-------------+------+-----+---------+-------+--------------------+
		| id       | char(64)    | NO   | PRI | NULL    |       |  session id (hex)  |
		| user     | int(11)     | YES  |     | NULL    |       |      user id       |
		| username | varchar(32) | YES  |     | NULL    |       |      username      |
		| access   | int(11)     | YES  |     | NULL    |       |  user access level |
		| expire   | datetime    | YES  |     | NULL    |       | session expiration |
		| context  | varchar(32) | YES  |     | NULL    |       |    user context    |
		| history  | text        | YES  |     | NULL    |       |  user cmd history  |
		| cmd      | varchar(16) | YES  |     | NULL    |       |  continued command |
		| cmddata  | text        | YES  |     | NULL    |       |   command's data   |
		+----------+-------------+------+-----+---------+-------+--------------------+
	
	table users
		+----------+-------------+------+-----+---------+----------------+-------------------+
		| Field    | Type        | Null | Key | Default | Extra          |   Description     |
		+----------+-------------+------+-----+---------+----------------+-------------------+
		| id       | int(11)     | NO   | PRI | NULL    | auto_increment |     user id       |
		| username | varchar(32) | YES  |     | NULL    |                |     username      |
		| password | char(64)    | YES  |     | NULL    |                |  hashed password  |
		| access   | int(11)     | YES  |     | NULL    |                | user access level |
		+----------+-------------+------+-----+---------+----------------+-------------------+
	
	table wall
		+--------+-----------+------+-----+-------------------+-------+--------------+
		| Field  | Type      | Null | Key | Default           | Extra | Description  |
		+--------+-----------+------+-----+-------------------+-------+--------------+
		| user   | int(11)   | YES  |     | NULL              |       |   user id    |
		| text   | text      | YES  |     | NULL              |       | note content |
		| posted | timestamp | NO   |     | CURRENT_TIMESTAMP |       | posting time |
		+--------+-----------+------+-----+-------------------+-------+--------------+

Access Levels:
	-10 - banned, can't see
	-1 - banned, still visible
	0 - guest
	10 - normal user
	20 - halfmod
	30 - mod
	40 - admin
	50 - owner

All files are to be kept at api.u413.com
These are not the files which are to be kept at public_html (or www) to run the site
They are not part of the api and hence not part of the current project. They are however , required to run u413
To get those scripts , you can PM/email PiMaster who is the current Administartor of u413 at darknut83@gmail.com
Or download them yourself.

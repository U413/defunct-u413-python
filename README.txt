u413 - an open-source BBS/terminal/PI-themed forum
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
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

Boards:
	i -- Imaginary* ?
	-1 -- Negative*
	0 -- All
	1 -- Links
	2 -- Programming
	3 -- Anon
	4 -- Site
	5 -- Video/movies
	6 -- Audio/music
	7 -- Literature
	8 -- Math
	9 -- Science/skepticism
	10 -- Foreign
	11 -- Misc
	20 -- Brony (20% cooler)*
	33 -- Religion/spiritualism
	37 -- Comic (first xkcd comic with "My hobby")*
	42 -- Life the Universe and Everything*
	69 -- NSFW (special behavior - doesn't show up in board 0)
	117 -- Halo (Master Chief's number)*
	151 -- Anime (151 original pokemon)*
	278 -- E*
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
	[transmit]text[/transmit] - Formats the text so that clicking it puts it in the prompt. *
	[color=HEX]text[/color] - Formats the text so that it's in color (Note: Only hex values are supported) *
	SHIFT + ENTER - Drop down a line in forum posts.
	
	[video]link[/video] - Displays a video (video formats, NOT FOR YOUTUBE) (NOTE: figure out a way to make this like u413.tv).
	[youtube]link/id[/video] - Displays a youtube video (NOTE: May be deprecated in the future).
	[audio]link[/audio] - Plays audio (with controls - no autoplay).
	[flash]link[/flash] - Embeds a flash animation/game.
	[js]code[/js] - Embeds javascript in an iframe.
	[css=code]text[/css] - Styles text.
	[spoiler(=label)]text[/spoiler] - Hides text under a label until the user clicks a button.
	[list=start (ex: a A 1, none means unordered)][*]item 1 [*]item 2 [*] item 3 [/list] - Make an ordered or unordered list.
	[table][row][column]stuff[/column][/row][/table] - Build a table.

import cmd
import display

help='''-= Global Commands =-
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
	[table][row][column]stuff[/column][/row][/table] - Build a table.'''

#build display items
items=[]
for line in help.slpl

def cmd_init(user,args):
	tmp=user.json.copy()
	tmp.update({"Command":"HELP","DisplayItems":[
		display.DisplayItem(text="Welcome to..."),
		dispaly.DisplayItem(text=logo,donttype=True),
		display.DisplayItem(text='Type "HELP" to begin.')
	])

Command("INITIALIZE","Initialize the terminal",cmd_init)

import optparse

cmds={}

class Command(optparse.OptionParser):
	def __init__(self,name,description,func,level=0,help=False):
		super(type(self),self).__init__(description)
		cmd=name.upper()
		cmds.update({cmd:self})
		self.name=cmd
		self.description=description
		self.response=func
		self.level=level
		self.help=help

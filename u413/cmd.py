import argparse

cmds={}

class Command(argparse.ArgumentParser):
	def __init__(self,name,description,func,level=0,context=None,help=False):
		super(argparse.ArgumentParser,self).__init__(description)
		cmds.update({name.upper():self})
		self.response=func

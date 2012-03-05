class Item(dict):
	def __init__(self,text,mute=False,donttype=False):
		super(type(self),self).__init__(text=text,mute=mute,donttype=donttype)
		self.text=text
		self.mute=mute
		self.donttype=donttype

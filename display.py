class Item(dict):
	def __init__(self,text,mute=False,donttype=False):
		super(type(self),self).__init__(Text=text,Mute=mute,DontType=donttype)

import cgi
import hashlib
import uuid

import database

def sha256(data):
	return hashlib.sha256(data).hexdigest()

class User(object):
	banned=-1
	guest=0
	member=10
	mod=20
	admin=30
	def __init__(self):
		self.username=''
		self.session=''
		self.level=0
		self.userid=0
	
	def login(self,username,password):
		password=sha256(password)
		r=database.query("SELECT * FROM users WHERE username='%s' AND password='%s';"%(database.escape(username),password)
		if len(r)==0:
			return False
		r=r[0]
		self.username=r["username"]
		self.session=uuid.uuid4()
		self.level=r["access"]
		self.userid=r["id"]
		database.query("INSERT INTO sessions (id,user,expire) VALUES('%s',%s,'%s');"%(self.session,self.userid,time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime()))
	
	def logout(self):
		if self.session!='':
			database.query("DELETE FROM sessions WHERE id='%s';"%self.session

import socket
import hashlib
import base64 as b64


class WebSocket(object):
	handshake_header='HTTP/1.1 101 Web Socket Protocol Handshake\r\nUpgrade: WebSocket\r\nConnection: Upgrade\r\nWebSocket-Origin: %s\r\nWebSocket-Location: %s\r\nSec-WebSocket-Accept: %s\r\n%s\r\n'
	guid="258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

	def __init__(self):
		self.socket=socket.socket()
		self.socket.bind(('',1413))
	
	def handshake(self,client):
		handshake=client.recv(1024)
		print handshake
		handshake=handshake.split('\r\n')
		rows={}
		i=0
		while i<len(handshake):
			parts=handshake[i].split(':',1)
			if len(parts)==2:
				rows.update({parts[0].strip().lower():parts[1].strip()})
			i+=1
		print rows
		key=rows["sec-websocket-key"]
		protocol=''
		if 'sec-websocket-protocol' in rows:
			protocol='Sec-WebSocket-Protocol: %s\r\n'%rows["sec-websocket-protocol"]
		accept=b64.b64encode(hashlib.sha1(key+WebSocket.guid).digest())
		s=WebSocket.handshake_header%(rows['origin'],'ws://'+rows['host'],accept,protocol)
		print s
		self.socket.send(s)
	
	def run(self):
		self.socket.listen(4)
		client,addr=self.socket.accept()
		self.handshake(client)
		self.send('SEND Hello%20world! Server')
	
	def send(self,s):
		self.socket.sendall('\x00%s\xff'%s)
	
	def recv(self):
		s=''
		m=''
		while True:
			m=self.socket.recv(4096)
			if m[-1]=='\xff':
				s+=m[:-1]
				break
			s+=m
		return s

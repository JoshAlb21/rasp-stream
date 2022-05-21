import socket

s = socket.socket()		 
print ("Socket successfully created") 

port = 10001#65335			

s.bind(('', port))
print ("socket binded to %s" %(port)) 

s.listen(5)	 
print ("socket is listening")

c, addr = s.accept()	 
print ('Got connection from', addr ) 

c.send(b'Thank you for connecting') 

c.close()
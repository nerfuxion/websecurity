# -*- coding: cp1252 -*-
#https://github.com/nerfuxion/sslsecurity
#RedShield - Written by Fredrik Söderlund
#www.redshield.co

import socket

SOMAXCONN = 128

serverIp = ""
serverPort = 1234
inputBufferSize = 1024
userListFile = "secrets/userlist"
credentialsFile = "etc/dbcredentials"
noAccess = "NO"
noUserList = "*********\n"
okAccess = "OK"



#Try to read the credentials that protects the database secrets
try:
    fileDescriptor = open(credentialsFile, "r")
    fileContent = fileDescriptor.read()
    fileDescriptor.close()
   
except:
    print("error no database credentials")


dbCredentials = fileContent.split(":")
userName = dbCredentials[0]
userPassword = dbCredentials[1]

#report that database is active
print("database active")


#create the database socket, listening on port 1234
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
serverSocket.bind((serverIp, serverPort))
serverSocket.listen(SOMAXCONN)

#database io loop, accepts any incoming connection
while(1 == 1):
    acceptSocket, acceptAddress = serverSocket.accept()

    #read incoming username    
    userNameIncoming = acceptSocket.recv(inputBufferSize)
    userNameIncoming = str(userNameIncoming, 'ascii')

    if(userNameIncoming == userName):
        acceptSocket.send(bytes(okAccess, 'ascii'), len(okAccess))

        #read incoming password
        userPasswordIncoming = acceptSocket.recv(inputBufferSize)
        userPasswordIncoming = str(userPasswordIncoming, 'ascii')

        if(userPasswordIncoming == userPassword):
            acceptSocket.send(bytes(okAccess, 'ascii'), len(okAccess))
            print("login allowed")

            #login was allowed, read userlist from secrets folder and send to whoever asked for it    
            print("userlist request from ip: " + str(acceptAddress[0]) + " on port: " + str(acceptAddress[1]))

            try:
                fileDescriptor = open(userListFile, "rb")
                fileContent = fileDescriptor.read()
                acceptSocket.send(fileContent)
                fileDescriptor.close()
                acceptSocket.close()
            except:
                print("userListFile not found")
                acceptSocket.close()
        else:            
            acceptSocket.send(bytes(noAccess, 'ascii'), len(noAccess))   
            print("login denied - bad password")
            acceptSocket.send(bytes(noUserList, 'ascii'), len(noUserList))
    else:            
        acceptSocket.send(bytes(noAccess, 'ascii'), len(noAccess))
        userPasswordIncoming = acceptSocket.recv(inputBufferSize)
        acceptSocket.send(bytes(noAccess, 'ascii'), len(noAccess))   
        print("login denied - bad username")
        acceptSocket.send(bytes(noUserList, 'ascii'), len(noUserList))

serverSocket.close()




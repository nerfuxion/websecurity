# -*- coding: cp1252 -*-
#https://github.com/nerfuxion/websecurity
#RedShield - Written by Fredrik Söderlund
#www.redshield.co

import socket
import sys


#Function that builds a html doc populated with user names retrieved from database
userListBegin = '<!DOCTYPE html>\r\n'\
             '<html>\r\n'\
             '<body>\r\n'\
             '<h2>System Users:</h2>\r\n'

userListEnd = '<a href="/">Back to start page </a>\r\n'\
             '</body>\r\n'\
             '</html>\r\n'

def generateUserList():

    print("generating userlist.htm")
	
    userList = databaseLoginAndGetUserList()	

    userName = userList.split('\r\n')
    userName = userList.split('\n')
    nameList = ""

    i=0
    while(1 == 1):
        try:
            currentName = userName[i]
            currentName = "<p>" + currentName + "</p>"
            nameList = nameList + currentName
            i=i+1
        except:
            break
 
    userListPage = userListBegin + nameList + userListEnd
    return userListPage
    



    
#Function that retrieves user name list from database    
dbHost = ""
dbPort = 1234
credentialsFile = "etc/dbcredentials"

def databaseLoginAndGetUserList():
    try:
        fileDescriptor = open(credentialsFile, "r")
        fileContent = fileDescriptor.read()
        fileDescriptor.close()
       
    except:
        print("error no database credentials")
        return

    dbCredentials = fileContent.split(":")
    userName = dbCredentials[0]
    userPassword = dbCredentials[1]
    
    dbSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dbSocket.connect((dbHost, dbPort))

    dbSocket.send(bytes(userName, 'ascii'), len(userName))
    response = dbSocket.recv(1024)
    
    dbSocket.send(bytes(userPassword, 'ascii'), len(userPassword))
    response = dbSocket.recv(1024)

    response = dbSocket.recv(1024)
    dbSocket.close()
    
    response = str(response, 'ascii')
    return response
    



    
#Main server function    
SOMAXCONN = 128
serverIp = ""
serverPort = 80
inputBufferSize = 1024
defaultErrorFile = "www/404.html"

#Check if the database IP address has been supplied
if len(sys.argv) <= 1:
  print('usage: python webserver.py <database ip>')
  sys.exit()

dbHost = sys.argv[1]

#Report that webserver is active
print("webserver active")

#Create webserver socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
serverSocket.bind((serverIp, serverPort))
serverSocket.listen(SOMAXCONN)

#Main webserver loop, accepts incoming connections and serves up web pages from www folder
while(1 == 1):
    acceptSocket, acceptAddress = serverSocket.accept()
    incomingRequest = acceptSocket.recv(inputBufferSize)

    print("incoming request from ip: " + str(acceptAddress[0]) + " on port: " + str(acceptAddress[1]))

    incomingRequest = incomingRequest.decode("utf-8")
    requestedResource = incomingRequest.split(' ')

    try:
        requestedResource = requestedResource[1]
    except:
        requestedResource = "HTTP"
        print("unexpected unhandled request")

    requestedResource = requestedResource.split('HTTP')
    requestedResource = requestedResource[0]

    if(requestedResource == "/"):
        print("requesting root page")
        requestedResource = "/index.html"

    #If browser requests the user list, the webserver will log into the database and request it
    if(requestedResource == "/userlist.html"):
        requestedResource = "www" + requestedResource
        print("requested resource: " + requestedResource)
        userListPage = generateUserList()
        acceptSocket.send(bytes(userListPage, 'ascii'), len(userListPage))
        acceptSocket.close()
    else:  
        
        requestedResource = "www" + requestedResource
        print("requested resource: " + requestedResource)

        try:
            fileDescriptor = open(requestedResource, "rb")
        except:
            fileDescriptor = open(defaultErrorFile, "rb")

        fileContent = fileDescriptor.read()
        acceptSocket.send(fileContent)
        fileDescriptor.close()
        acceptSocket.close()

serverSocket.close()

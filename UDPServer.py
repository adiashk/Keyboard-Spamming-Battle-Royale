from socket import *
serverPort = 12005
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print("Server started, listening on IP address 172.1.0.4")
# “offer” announcements via UDP broadcast once every second
while True:
    print("--")
    message, clientAddress = serverSocket.recvfrom(2048)
    print("----")
    print (message)
    modifiedMessage = message.upper()	
    serverSocket.sendto(modifiedMessage, clientAddress)

from socket import *
serverName = 'hostname'
serverPort = 12004
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = input("Input lowercase sentence:")
clientSocket.sendto(message.encode('utf-8'),('', serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print (modifiedMessage)
clientSocket.close()

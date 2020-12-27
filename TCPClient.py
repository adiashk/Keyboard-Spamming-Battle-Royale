from socket import *
serverName = ""
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
sentence = input("Input lowercase sentence:")
clientSocket.send(sentence.encode('utf-8'))
# clientSocket.sendto(sentence,(serverName, serverPort))
modifiedSentence = clientSocket.recv(1024)
print ("From Server:", modifiedSentence)
clientSocket.close()

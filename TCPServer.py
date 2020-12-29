from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
ip = gethostbyname(gethostname())
print(ip)
# serverSocket_TCP_Master.bind((ip,serverPort))
serverSocket.bind((ip,serverPort))
serverSocket.listen(1)
print ("The server is ready to receive")
while True:
     connectionSocket, addr = serverSocket.accept()
     sentence = connectionSocket.recv(1024)
     capitalizedSentence = sentence.upper()
     connectionSocket.send(capitalizedSentence)
     connectionSocket.close()

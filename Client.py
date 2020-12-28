from socket import *
print ("Client started, listening for offer requests...")
serverPort = 13117
while True:
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    clientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    clientSocket.bind(('', serverPort))
    message, serverAddress = clientSocket.recvfrom(2048)
    print("message= ",message)
    print("serverAddress= ", serverAddress)
    print("----------")
    clientSocket.close()
    
    print("Received offer from ", serverAddress, " attempting to connect...")
    serverPort = message[13:].decode('utf-8')
    # GAME
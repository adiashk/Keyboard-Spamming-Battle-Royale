from socket import *
team_name = "yuval_adi"

def UDP_connection():    
    print ("Client started, listening for offer requests...")
    serverPort = 13117
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    clientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    clientSocket.bind(('', serverPort))
    message, serverAddress = clientSocket.recvfrom(2048)
    print("message= ",message)
    print("serverAddress= ", serverAddress)
    clientSocket.close()
    return message, serverAddress

def TCP_connection(message, serverAddress, team_name):
    print("Received offer from ", serverAddress, " attempting to connect...")
    serverPort = message[13:].decode('utf-8')
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(('', serverPort))
    clientSocket.send(team_name.encode('utf-8'))
    while True: # receive welcome message
        open_game_massage = clientSocket.recv(1024).decode()
        if open_game_massage:
            print(open_game_massage)
            break
    # GAME!
    while True: # read and then write to socket
        stop_mssage = clientSocket.recv(1024).decode()
        if stop_mssage:
            print(stop_mssage)
            break
        clientSocket.send(getch.getche().encode())
        print()

    clientSocket.close()

while True:
    message, serverAddress = UDP_connection()
    TCP_connection(message, serverAddress, team_name)

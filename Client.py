from socket import *
import struct
# import getch
# team_name = "yuval_adi"

def UDP_connection():
    clientSocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    clientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    serverPort = 13117
    clientSocket.bind(('', serverPort))
    print ("Client started, listening for offer requests...")
    while True:   
        try:
            message, serverAddress = clientSocket.recvfrom(1024)    
            unpacked_message = struct.unpack('QQQ', message)    
            print(str(unpacked_message[0])) 
            if unpacked_message[0] == 4276993775:   
                clientSocket.close()    
                print("aaa")    
                server_tcp_port = unpacked_message[2]   
                (ip, port) = serverAddress  
                print(server_tcp_port)  
                print(ip)   
                ip ='172.1.0.94'    
                return ip, server_tcp_port  
        except:
            continue


def TCP_connection(ip, server_tcp_port):
    print("Received offer from ", ip, " attempting to connect...")
    # server_tcp_port = message[13:].decode('utf-8')
    # message_content = struct.unpack('Ibh', message)
    # server_tcp_port = message_content[2]
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((ip, server_tcp_port))
    team_name = input("enter name:")
    clientSocket.send(team_name.encode('utf-8'))
    while True: # receive welcome message
        open_game_massage = clientSocket.recv(1024).decode()
        if open_game_massage:
            print(open_game_massage)
            break
    # GAME!
    while True:  # read and then write to socket
        stop_mssage = ''
        try:
            stop_mssage = clientSocket.recv(1024).decode()
            print(stop_mssage)

        except:
            # char = getch.getche()
            char = 'a'
            # char = msvcrt.getche()
            print(char)
            clientSocket.send(char.encode('utf-8'))

            # with Input(keynames="curtsies", sigint_event=True) as input_generator:
            #     key = input_generator.send(0.1)
            #     if key:
            #         print(key)
            #         clientSocket.send((key + '\n').encode('utf-8'))
            if stop_mssage == "game over":
                print(stop_mssage)
                break

    # clientSocket.close()

while True:
    ip, server_tcp_port = UDP_connection()
    TCP_connection(ip, server_tcp_port)
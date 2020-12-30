from socket import *
import struct
import msvcrt

# team_name = "yuval_adi"

def UDP_connection():
    clientSocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    clientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    serverPort = 13006
    clientSocket.bind(('', serverPort))
    while True:   
        print ("Client started, listening for offer requests...")
        #print("udp")
        message, serverAddress = clientSocket.recvfrom(1024)
        unpacked_message = struct.unpack('QQQ', message)
        print(str(unpacked_message[0]))
        if unpacked_message[0] == 4276993775:
            clientSocket.close()
            print("aaa")
            return message, serverAddress


def TCP_connection(message, serverAddress):
    (ip, port) = serverAddress
    print("Received offer from ", ip, " attempting to connect...")
    # serverPort = message[13:].decode('utf-8')
    message_content = struct.unpack('QQQ', message)
    serverPort = message_content[2]
    clientSocket = socket(AF_INET, SOCK_STREAM)
    # ip = gethostbyname(gethostname())
    print(ip)
    clientSocket.connect((ip, serverPort))
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
            # clientSocket.send(getch.getche().encode())
            # print("in except")
            # char = msvcrt.getche()
            # print(char)
            # clientSocket.send(char)
            with Input(keynames="curtsies", sigint_event=True) as input_generator:
                key = input_generator.send(0.1)
                if key:
                    print(key)
                    clientSocket.send((key + '\n').encode('utf-8'))
            if stop_mssage is "game over":
                print(stop_mssage)
                break

    # clientSocket.close()
    # def game_mode():
    #     with Input(keynames="curtsies", sigint_event=True) as input_generator:
    #     try:
    #         while is_palying:
    #             key = input_generator.send(0.1)
    #             if key:
    #                 print(key)
    #                 conn_tcp.send((key + '\n').encode('utf-8'))
    #     except Exception:
    #         return

while True:
    message, serverAddress = UDP_connection()
    TCP_connection(message, serverAddress)

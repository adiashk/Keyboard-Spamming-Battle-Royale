from socket import *
import struct
# import getch
import keyboard
message_code = 4276993775
def UDP_connection():
    """
    :return: ip of the server and tcp port of server
    """
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
            # print(str(unpacked_message[0]))
            if unpacked_message[0] == message_code:
                clientSocket.close()    
                server_tcp_port = unpacked_message[2]
                (ip, port) = serverAddress
                return ip, server_tcp_port  
        except:
            continue


def TCP_connection(ip, server_tcp_port):
    """
    :param ip: ip of the server
    :param server_tcp_port: tcp port of server
    :return: brake when server crash
    """
    print("Received offer from ", ip, " attempting to connect...")
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((ip, server_tcp_port))
    team_name = input("enter name:")
    clientSocket.send(team_name.encode('utf-8'))
    while True: # receive welcome message
        open_game_massage = clientSocket.recv(1024).decode()
        if open_game_massage:
            print(open_game_massage)
            break
    """
    game: read key and then write to socket
    """
    while True:
        # stop_message = ''
        # try:
            stop_message = clientSocket.recv(1024).decode()
            # print(stop_message)
            # if key:
            #     send_key = bytes(key, 'utf-8')
            #     clientSocket.sendall(send_key)
            if stop_message == "true":
                # print(stop_message)
                break

        # except:
            # char = getch.getche()
            # char = input("enter name:")
            # # char = msvcrt.getche()
            # print(char)
            # clientSocket.send(char.encode('utf-8'))

            key = keyboard.read_key()
            if key:
                send_key = bytes(key, 'utf-8')
                try:
                    clientSocket.sendall(send_key)
                except:
                    break  # back to udp connection
            # if stop_message == "game over":
            #     print(stop_message)
            #     break

    # clientSocket.close()

while True:
    ip, server_tcp_port = UDP_connection()
    TCP_connection(ip, server_tcp_port)

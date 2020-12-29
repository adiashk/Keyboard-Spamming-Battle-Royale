from socket import *
import threading
import time
from collections import defaultdict 

serverPort = 13117
serverSocket_UDP = socket(AF_INET, SOCK_DGRAM)
serverSocket_UDP.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket_UDP.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

serverSocket_TCP = socket(AF_INET,SOCK_STREAM)
serverSocket_TCP.bind(('',serverPort))
serverSocket_TCP.listen(1)

clients_group1 = defaultdict(int)
clients_group2 = defaultdict(int)
groups_counter = 0

def start_server():
    print("Server started, listening on IP address 172.1.0.4")
    start_time = time.time()
    while time.time() - start_time < 10:
        offer_UDP_connection()
    game()


def offer_UDP_connection():
    message = "0xfeedbeef" + "0x2" + "12000"
    threading.Timer(1.0, print_offers).start()
    serverSocket_UDP.sendto(message.encode('utf-8'), ('', serverPort))
    TCP_connection()


def TCP_connection():
    connectionSocket, addr = serverSocket_TCP.accept()
    team_name = connectionSocket.recv(1024)
    groups_counter += 1
    if groups_counter % 2 == 1:
        clients_group1[team_name] = 0
    elif
        clients_group2[team_name] = 0

def game():
    print_game_start()
    message = "Start pressing keys on your keyboard as fast as you can!!"
    

def print_game_start():
    print("Welcome to Keyboard Spamming Battle Royale.")
    print("Group 1:")
    print("==")
    for name in clients_group1.keys():
        print(name)
    print("Group 2:")
    print("==")
    for name in clients_group2.keys():
        print(name)
    


start_server()


# magic_cookie = 0xfeedbeef
# message_type= 0x2
# message = struct.pack('bbb', magic_cookie, message_type,localPort)

from socket import *
import threading
import _thread
import time
from collections import defaultdict 
import struct
from scapy.arch import get_if_addr
serverPort = 13006
serverSocket_UDP = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
serverSocket_UDP.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket_UDP.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

serverSocket_TCP_Master = socket(AF_INET, SOCK_STREAM)
# ip = gethostbyname(gethostname())
# print(ip)
server_ip = get_if_addr('eth1')

serverSocket_TCP_Master.bind((server_ip,serverPort))
serverSocket_TCP_Master.listen(1)


clients_group1 = defaultdict(list)
clients_group2 = defaultdict(list)
groups_counter = 0
stop_game = False
server_tcp_port = 2008
num_of_threads = []

def start_server():
    print("Server started, listening on IP address 172.1.0.4")
    stop_game = True
    # start_time = time.time()
    # while time.time() - start_time < 10:
            # offer_UDP_connection()
    # while stop_game:            
    #     _thread.start_new_thread ( offer_UDP_connection, ())
    #     _thread.start_new_thread ( TCP_connection, ())
    try:
        num_of_threads.append(1)
        _thread.start_new_thread(offer_UDP_connection, ())
    except Exception as err:
        print(err)
    try:
        num_of_threads.append(1)
        _thread.start_new_thread(TCP_connection, ())
    except Exception as err:
        print(err)
    while len(num_of_threads) > 0:
        pass

    # offer_UDP_connection()
    # TCP_connection()
    game()


def offer_UDP_connection():
    # message = "0xfeedbeef" + "0x2" + "12000"
    start_time = time.time()
    while time.time() - start_time < 10:
        message = struct.pack('QQQ',0xfeedbeef ,0x2, server_tcp_port)
        # threading.Timer(1.0, offer_UDP_connection).start()
        serverSocket_UDP.sendto(message, ('<broadcast>', serverPort))
        print("udp")
        time.sleep(1)
        # TCP_connection()
    num_of_threads.pop()


def TCP_connection():
    start_time = time.time()
    while time.time() - start_time < 10:
        print("tcp1")
        connection_socket, client_addr = serverSocket_TCP_Master.accept()
        print("tcp2")
        team_name = connection_socket.recv(1024)
        groups_counter += 1
        if groups_counter % 2 == 1:
            clients_group1[team_name].append(0, connection_socket, client_addr) # score=0
        else:
            clients_group2[team_name].append(0, connection_socket, client_addr) # score=0
    num_of_threads.pop()

def game():
    print_game_start()
    open_game_massage = "Start pressing keys on your keyboard as fast as you can!!"
    for team_name, client in clients_group1.items():  # (score, connection_socket, client_addr)
        connection_socket = client[1]
        client_addr = client[2]
        connection_socket.send(open_game_massage.encode('utf-8'))
        _thread.start_new_thread(game_of_client, (team_name, 1, connection_socket, client_addr))
        
    for team_name, client in clients_group2.items():  # (score, connection_socket, client_addr)
        connection_socket = client[1]
        client_addr = client[2]
        connection_socket.send(open_game_massage.encode('utf-8'))
        _thread.start_new_thread ( game_of_client, (team_name, 2, connection_socket, client_addr))

    time.sleep(10)
    stop_game = True
    print("Game over!")
    score1, score2 = calculate_score()
    if score1 > score2:
        g = 1
    else:
        g = 2
    print("Group 1 typed in ", score1, " characters. Group 2 typed in ", score2,
    " characters.Group ", g ," wins!")
    print("Congratulations to the winners:")
    print("==")
    if g == 1:
        for name in clients_group1.keys():
            print(name)
    else:
        for name in clients_group2.keys():
            print(name)
    print("Game over, sending out offer requests...")

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

def game_of_client(team_name, group_num, connection_socket, client_addr):
    while not stop_game:
        key = connection_socket.recv(1)
        if group_num == 1:
            clients_group1[team_name][0] += 1
        elif group_num == 2:
            clients_group2[team_name][0] += 1
    print("Server disconnected, listening for offer requests...")
    connection_socket.close()

def calculate_score():
    score1, score2 = 0
    for team_name, client in clients_group1.items():  # (score, connection_socket, client_addr)
        score1 += client[0]
    for team_name, client in clients_group2.items():
        score2 += client[0]
    return score1, score2

print("start")
start_server()
serverSocket_UDP.close()
serverSocket_TCP_Master.close()

# magic_cookie = 0xfeedbeef
# message_type= 0x2
# message = struct.pack('bbb', magic_cookie, message_type,localPort)

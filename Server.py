from socket import *
import _thread
import time
from collections import defaultdict 
import struct
# from scapy.arch import get_if_addr
serverPort = 13117
server_tcp_port = 2094
serverSocket_UDP = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
serverSocket_UDP.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

serverSocket_TCP_Master = socket(AF_INET, SOCK_STREAM)
# server_ip = get_if_addr('eth1')
server_ip = gethostbyname(gethostname())
serverSocket_TCP_Master.bind((server_ip,server_tcp_port))
magic_cookie = 0xfeedbeef
message_type = 0x2

clients_group1 = defaultdict(list)
clients_group2 = defaultdict(list)
stop_game = False
num_of_threads = []
connection_time = 10
game_time = 10

def start_server():
    print("Server started, listening on IP address ", server_ip)
    connection = False
    start_time = time.time()
    while time.time() - start_time < connection_time:
        if not connection:
            connection = True
            _thread.start_new_thread(offer_UDP_connection, (start_time,))
            _thread.start_new_thread(TCP_connection, (start_time,))
    game()


def offer_UDP_connection(start_time):
    """
    send broadcast to get udp connection
    :param start_time: when the connection open
    :return: finish after the given time
    """
    while time.time() - start_time < connection_time:
        message = struct.pack('QQQ', magic_cookie, message_type,server_tcp_port)
        serverSocket_UDP.sendto(message, ('<broadcast>', serverPort))
        time.sleep(1)  # send offer every second


def TCP_connection(start_time):
    """
    do tcp connection, get connection_socket and save it for each client
    :param start_time: when the connection open
    :return: finish after the given time
    """
    while time.time() - start_time < connection_time:
        serverSocket_TCP_Master.listen()
        connection_socket, client_addr = serverSocket_TCP_Master.accept()

        team_name = connection_socket.recv(1024).decode('utf-8')
        if len(clients_group1) == len(clients_group2):
            clients_group1[team_name] = [0, connection_socket, client_addr]  # start_score=0
        else:
            clients_group2[team_name] = [0, connection_socket, client_addr]  # start_score=0

def game():
    """
    start the game and send message to the clients, each client get thread that start the game
    print the score in the end
    :return:
    """
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
        _thread.start_new_thread(game_of_client, (team_name, 2, connection_socket, client_addr))

    time.sleep(game_time)
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
    """
    each client has separate thread- this is his game
    :param team_name: the name the client gave
    :param group_num: 1 or 2
    :param connection_socket: the client socket
    :param client_addr: the client address
    :return:
    """
    while not stop_game:
        connection_socket.send(str(stop_game).encode('utf-8'))
        key = connection_socket.recv(1024)
        # print(key)
        if group_num == 1:
            clients_group1[team_name][0] += 1
            # print(group_num)
        elif group_num == 2:
            clients_group2[team_name][0] += 1
            # print(group_num)
    print("Server disconnected, listening for offer requests...")
    stop_message = "game over"
    connection_socket.send(stop_message.encode('utf-8'))

    # connection_socket.close()

def calculate_score():
    """
    :return: score of each group
    """
    score1 = 0
    score2 = 0
    for team_name, client in clients_group1.items():  # (score, connection_socket, client_addr)
        score1 += client[0]
    for team_name, client in clients_group2.items():
        score2 += client[0]
    return score1, score2

while True:
    # print("start")
    start_server()
# serverSocket_UDP.close()
# serverSocket_TCP_Master.close()



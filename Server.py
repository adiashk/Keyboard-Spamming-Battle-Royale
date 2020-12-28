from socket import *
import threading
import time

def start_server():
    print( "Server started, listening on IP address 172.1.0.4")
    print_offers()

def print_offers():
    serverPort = 13117
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    message = "0xfeedbeef" + "0x2" + "12000"
    threading.Timer(1.0, print_offers).start()
    serverSocket.sendto(message.encode('utf-8'), ('', serverPort))


start_server()
import socket
import threading
import random

#the port of communication
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = socket.gethostbyname(socket.gethostname())
port = 1234
DISCONNECT_MSG = "disconnected!"
server_socket.bind((hostname, port))
clients_sockets = []
server_socket.listen(5)
print(f"server {hostname}: listening on port {port} ....")

def clients_connections_handler(client_socket, address):
    global clients_sockets
    possible_poses = ['11', '21', '31', '12', '22', '32', '13', '23', '33']
    while True:
        msg = client_socket.recv(1024)
        if msg and msg.decode() != DISCONNECT_MSG:
            print(f"{address}: {msg.decode()} ")
            for sock in clients_sockets:                
                if (str(msg.decode())) in possible_poses or (msg.decode() == "you win!") or (msg.decode() == "you lose!") :
                    if sock != client_socket:
                        sock.send(msg)
                        print(f"send: {msg} to:{address}")
                else:
                    sock.send(msg)
                    print(f"send not pos: {msg}")
                    
        elif msg.decode():
            clients_sockets[0].close()
            clients_sockets[1].close()
            break


def x_or_o():
    options = ["x", "o"]
    first_rand_choice = random.choice(options)
    options.remove(first_rand_choice)
    second_rand_choice = "".join(options)
    return first_rand_choice, second_rand_choice


while True:
    client_socket, address = server_socket.accept()
    print(f"{address[1]}: is connected...")
    clients_sockets.append(client_socket)
    if len(clients_sockets) == 2:
        first_rand_choice, second_rand_choice = x_or_o()
        clients_sockets[0].send(bytes(first_rand_choice, encoding="utf-8"))
        clients_sockets[1].send(bytes(second_rand_choice, encoding="utf-8"))
    else:
        client_socket.send(bytes("[SERVER] is waiting for another player...", encoding="utf-8"))



    #creaing a thread for each client_socket connection so many clients will be able to connect at once
    client_thread = threading.Thread(target = clients_connections_handler, args=(client_socket, address))
    #setting a parameter that allows to stop running the program even a thread is still processing
    client_thread.daemon = True
    #starting the thread
    client_thread.start()





import socket
import threading




#the port of communication
WAIT_MSG = "[SERVER] is waiting for another player..."

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

hostname = socket.gethostbyname(input("Enter server ip address: "))
port = 5050
client_socket.connect((hostname, port))
print(f"You connected to {hostname}")
msg = ""
checked_once = False

def receive_msg():
    received_msg = client_socket.recv(2048)
    return received_msg


def send_msg(msg=""):
    client_socket.send(bytes(msg, encoding="utf-8"))

send_thread = threading.Thread(target=send_msg)
send_thread.daemon = True
send_thread.start()


messages = []

def main():
    run = True
    global msg
    while run:
        msg = receive_msg()
        if msg:
            messages.append(msg.decode())
        else:
            client_socket.close()
            run = False

    #creating a thread so you can receive and send messages at the same time.
    #the sending process will work at the background


if __name__ == "__main__":
    main()

















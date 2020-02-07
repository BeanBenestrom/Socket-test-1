import socket
import threading
import time
import pickle
import colorama as color

color.init()

green = color.Fore.GREEN
yellow = color.Fore.LIGHTYELLOW_EX
red = color.Fore.RED
white = color.Fore.WHITE

ip = socket.gethostname()
port = 7654
maxUsers = 3

Users = []
user_amount = 0

def create_server():
    try:
        global server
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((ip, port))
        server.listen(5)
    except socket.error:
        print("ERROR: Server could not be created!\n       Retrying...")
        time.sleep(1)
        create_server()


def remove_user(conn, address):
    global user_amount
    for user in Users:
        if user == [conn, address]:
            Users.remove(user)
            print(red + f"\n{address} removed!" + white)
            conn.close()
            user_amount -= 1


def messaging(conn, address):
    while True:
        try:
            msg = conn.recv(1024)
            if len(msg.decode()) > 1024:
                try:
                    conn.send(bytes(""))
                except socket.error:
                    print(yellow + "\nERROR: User, whom we are sending a message, does not exsist." + white)
                    remove_user(conn, address)
                    return
                messaging(conn, address)
        except socket.error:
            print(yellow + "\nERROR: User, whom we are receiving messages, does not exsist." + white)
            remove_user(conn, address)
            return

        for user in Users:
            try:
                d = pickle.dumps([address[0], msg.decode()])
                user[0].send(d)
            except socket.error:
                print(yellow + "\nERROR: User, whom we are sending a message, does not exsist." + white)
                remove_user(conn, address)
                return    


create_server()

while True:
    if maxUsers > user_amount: 
        conn, address = server.accept()
        Users.append([conn, address])
        print(green + f"User {address} connected!" + white)
        conn.send(bytes("------Welcome to the chat!------\n", "utf-8"))
        messageThread = threading.Thread(target=messaging, args=[conn, address])
        messageThread.start()
        user_amount += 1
    else:
        print("\nServer is full! \nBlocking all connection.")
        break

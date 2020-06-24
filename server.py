import socket
import threading
import time
import pickle
import colorama as color
import random

color.init()

green = color.Fore.GREEN
yellow = color.Fore.YELLOW
red = color.Fore.RED
white = color.Fore.WHITE

colorsDef = ["white", "green", "red", "cyan", "blue", "magenta"]
colors = ["white", "green", "red", "cyan", "blue", "magenta"]

ip = None
port = None
maxUsers = 3
#
Users = []
user_amount = 0
i = 0
full = False
maxTries = 4

#  + color.Fore.LIGHTBLUE_EX
# print(color.Fore.CYAN + "E" + color.Fore.LIGHTYELLOW_EX + "P" + color.Fore.YELLOW + "I" + color.Fore.LIGHTWHITE_EX + "C")
# + color.Fore.MAGENTA  + color.Fore.LIGHTMAGENTA_EX +  + color.Fore.BLUE

def addServer():
    global ip, port
    while True:
        ip = input("IP>")
        port = input("Port>")
        if ip == "":
            print("IP cannot be blank\n")
        else:
            try: 
                port = int(port)
                if 0 <= port <= 65535:
                    print(f"\n---IP:    {ip}")
                    print(f"---PORT:  {port}\n")
                    break
                else:
                    print("Port must be between 0-65535\n")
            except ValueError:
                print("Port should only be numbers\n")


def create_server():
    try:
        global server, i
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((ip, port))
        server.listen(5)
        print("\nServer created!\n")
    except socket.error:
        i += 1
        if i >= maxTries:
            i = 0
            print(red + f"\nERROR: Server could not be created after {maxTries} tries!" + white)
            print("Possibly the IP or the port is wrong.\n")
            addServer()
            create_server()
            return
        print(red + f"ERROR: Server could not be created!\n       Retrying...({i})" + white)
        time.sleep(0.5)
        create_server()   


def remove_user(conn, address):
    global user_amount, full
    for user in Users:
        if user == [conn, address]:
            Users.remove(user)
            print(yellow + f"\n{address} removed!" + white)
            conn.close()
            user_amount -= 1
            full = False
            for user in Users:
                sendMessage(user, ["SERVER:", ""], f"User {address[0]} left the chat!", "yellow")


def sendMessage(user, address, msg, colorIndex):
    try:
        d = pickle.dumps([address[0], msg, colorIndex])
        user[0].send(d)
    except socket.error:
        print(red + "\nERROR: User, whom we are sending a message, does not exsist." + white)
        remove_user(conn, address)
        return 


def messaging(conn, address, colorIndex):
    while True:
        try:
            msg = conn.recv(1024)
            if len(msg.decode()) > 1024:
                try:
                    conn.send(bytes(""))
                except socket.error:
                    print(red + "\nERROR: User, whom we are sending a message, does not exsist." + white)
                    remove_user(conn, address)
                    return
                messaging(conn, address, colorIndex)
        except socket.error:
            print(red + "\nERROR: User, whom we are receiving messages, does not exsist." + white)
            remove_user(conn, address)
            return
        for user in Users:
            sendMessage(user, address, msg.decode(), colorIndex)



def chooseColor():
    if len(colors) == 0:
        userColor = random.choice(colorsDef)
    else:
        userColor = random.choice(colors)
        colors.remove(userColor)
    return userColor


addServer()
create_server()

while True:
    if maxUsers <= user_amount and full == False: 
        full = True
        print("\nServer is full! \nBlocking all connections.")
    conn, address = server.accept()

    if full: 
        try:
            d = pickle.dumps(["SERVER: Server is full!    Try again later.", "yellow"])
            conn.send(d)
            conn.close()
        except socket.error:
            pass
    else:
        for user in Users:
            sendMessage(user, ["SERVER:", ""], f"User {address[0]} joined the chat!", "yellow")
        Users.append([conn, address])
        userColor = chooseColor() 
        print(green + f"User {address} connected!" + white)
        d = pickle.dumps(["------Welcome to the chat!------", "green"])
        conn.send(d)
        messageThread = threading.Thread(target=messaging, args=[conn, address, userColor])
        messageThread.start()
        user_amount += 1

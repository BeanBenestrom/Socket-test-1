import socket
import time
import sys
import os
import pickle
import threading
import colorama as color

color.init()

green = color.Fore.GREEN
white = color.Fore.WHITE
red = color.Fore.RED
yellow = color.Fore.LIGHTYELLOW_EX

colors = {
    "white" : color.Fore.WHITE,
    "green" : color.Fore.GREEN,
    "yellow" : color.Fore.YELLOW,
    "red" : color.Fore.RED,
    "cyan" : color.Fore.CYAN,
    "blue" : color.Fore.BLUE,
    "magenta" : color.Fore.MAGENTA,
}
#--------------------------------------------
ip = None # Add ip here (don't)? >=|
port = None

#--------------------------------------------
#
i = 0
queue = False
maxTries = 5
texts = []


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
                print(f"\n---IP:    {ip}")
                print(f"---PORT:  {port}\n")
                break
            except ValueError:
                print("Port should only be numbers\n")


def connect_to_server():
    global i
    global server
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((ip, port))
    except socket.error:
        i += 1
        if i >= maxTries:
            print(red + f"\nERROR: Could not connect to server after {maxTries} tries!" + white)
            print("Possibly the IP or the port is wrong.\n" + white)
            addServer()
            connect_to_server()
        print(red + f"ERROR: Could not connect to server!\n       Retrying...({i})" + white)
        time.sleep(0.5)
        connect_to_server()


def new_message():
    global queue
    while True:
        d = server.recv(1024)
        queue = True
        address, msg, userColor = pickle.loads(d)
        if msg != "":
            texts.append([colors.get(userColor) + f"{address}" + white, f"{msg}\n"])
            os.system("cls")
            for text in texts:
                print(text[0])
                print(f"    {text[1]}")
        queue = False


while True:
    addServer()
    connect_to_server()

    d = server.recv(1024)
    msg, userColor = pickle.loads(d)
    print(colors.get(userColor) + f"{msg}\n" + white)
    if msg.find("-") != -1:
        texts.append([colors.get(userColor) + msg + white, ""])
        break

messageTread = threading.Thread(target=new_message)
messageTread.start()

while True:
    if queue == True:
        time.sleep(0.1)
    else:
        user_input = input(">")
        if len(user_input) > 1024:
            print("\nMessage is too long!")
        elif user_input == "":
            pass
        else:
            server.send(bytes(user_input, "utf-8"))

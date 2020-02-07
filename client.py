import socket
import time
import sys
import os
import pickle
import threading
import colorama as color

green = color.Fore.GREEN
white = color.Fore.WHITE

#--------------------------------------------
ip = None # Add ip here
print("ADD AN IP TO CONNECT TO IN THE CODE")
time.sleep(3)
sys.exit()
#--------------------------------------------
port = 7654

i = 0
queue = False
maxTries = 5
texts = []


def connect_to_server():
    global i
    global server
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((ip, port))
    except socket.error:
        if i > maxTries:
            print(f"\nERROR: Could not connect to server after {maxTries} tries!\n       Try again later.")
            sys.exit()  
        print("ERROR: Could not connect to server!\n       Retrying...")
        i += 1
        time.sleep(1)
        connect_to_server()


def new_message():
    global queue
    while True:
        d = server.recv(1024)
        queue = True
        address, msg = pickle.loads(d)
        if msg != "":
            texts.append([address, msg])
            os.system("cls")
            for text in texts:
                print(text[0])
                print(f"    {text[1]}\n")
        queue = False

connect_to_server()

msg = server.recv(1024)
print(msg.decode())

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

import socket
import threading
from tkinter import *

class GUI:
    def __init__(self):
        self.window = Tk()
        self.window.title("Login")
        self.window.geometry("300x200")
        self.window.resizable(False, False)

        login_label = Label(self.window, text="Please login before continuing")
        login_label.place(relx=0.5, rely=0.5, anchor=CENTER)

        name_label = Label(self.window, text="Name:")
        name_label.place(x=50, y=100)

        name_entry = Entry(self.window)
        name_entry.place(x=100, y=100)

        login_button = Button(self.window, text="Login", command=lambda: self.goAhead(name_entry.get()))
        login_button.place(x=150, y=150)

        self.window.mainloop()

    def goAhead(self, name):
        self.window.destroy()
        self.name = name
        threading.Thread(target=self.receive).start()

    def receive(self):
        while True:
            try:
                message = client_socket.recv(1024).decode("utf-8")
                if message == "NICKNAME":
                    client_socket.send(self.name.encode("utf-8"))
                else:
                    pass
            except:
                print("An error occurred")
                client_socket.close()
                break

    def write(self):
        while True:
            message = input()
            client_socket.send(message.encode("utf-8"))

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    IP = "127.0.0.1"
    PORT = 12345
    client_socket.connect((IP, PORT))

    threading.Thread(target=receive).start()
    threading.Thread(target=write).start()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    IP = "127.0.0.1"
    PORT = 12345
    server_socket.bind((IP, PORT))
    server_socket.listen()

    nicknames = []

    def client_thread(client_socket, address):
        client_socket.send("NICKNAME".encode("utf-8"))
        nickname = client_socket.recv(1024).decode("utf-8")
        nicknames.append(nickname)

        while True:
            try:
                message = client_socket.recv(1024).decode("utf-8")
                if message:
                    print(message)
            except:
                index = nicknames.index(nickname)
                nicknames.pop(index)
                break

    while True:
        client_socket, address = server_socket.accept()
        threading.Thread(target=client_thread, args=(client_socket, address)).start()

start_server()

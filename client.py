import socket
from threading import Thread

# Client configuration
IP_ADDRESS = "127.0.0.1"
PORT = 12345

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((IP_ADDRESS, PORT))

# Ask the user to choose their nickname
nickname = input("Choose your nickname: ")
client_socket.send(f"NICKNAME {nickname}".encode('utf-8'))

def receive():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message.startswith("NICKNAME"):
                # Server sends the nickname back, print a confirmation
                print(f"Your nickname is set to: {nickname}")
            else:
                print(message)
        except Exception as e:
            print(f"An error occurred: {e}")
            client_socket.close()
            break

def write():
    while True:
        user_input = input()
        client_socket.send(user_input.encode('utf-8'))

# Start receive and write functions with threads
receive_thread = Thread(target=receive)
write_thread = Thread(target=write)

receive_thread.start()
write_thread.start()

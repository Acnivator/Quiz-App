import socket
from threading import Thread

# Server configuration
IP_ADDRESS = "127.0.0.1"
PORT = 12345

# List to maintain connected clients and their nicknames
clients = []
nicknames = []

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the server to the IP and Port
server_socket.bind((IP_ADDRESS, PORT))

# Listen for incoming connections
server_socket.listen(5)
print(f"Server listening on {IP_ADDRESS}:{PORT}")

def clientthread(client_socket, nickname):
    global clients, nicknames

    # Send a welcome message to the client
    client_socket.send("Welcome to the Quiz Game!".encode('utf-8'))

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                # If the message is empty, the client has disconnected
                remove_client(client_socket, nickname)
                break
            # Broadcast the message to all clients
            broadcast(f"{nickname}: {message}", client_socket)
        except Exception as e:
            print(f"An error occurred: {e}")
            remove_client(client_socket, nickname)
            break

def remove_client(client_socket, nickname):
    global clients, nicknames

    # Remove the client and their nickname from the lists
    clients.remove(client_socket)
    nicknames.remove(nickname)
    print(f"Client {nickname} disconnected.")

def broadcast(message, sender_socket):
    global clients

    # Send the message to all clients except the sender
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except Exception as e:
                print(f"An error occurred while broadcasting: {e}")
                remove_client(client, nicknames[clients.index(client)])

while True:
    # Accept incoming connection
    client_socket, addr = server_socket.accept()

    # Receive the nickname from the client
    nickname = client_socket.recv(1024).decode('utf-8')
    nicknames.append(nickname)

    # Add the client to the list
    clients.append(client_socket)

    # Send a welcome message to the client
    client_socket.send("Welcome to the Quiz Game!".encode('utf-8'))

    # Create a new thread for the client
    thread = Thread(target=clientthread, args=(client_socket, nickname))
    thread.start()

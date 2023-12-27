import socket
import threading

# Ask the user to choose their nickname
nickname = input("Enter your nickname: ")

# Create a client with AF_INET and SOCK_STREAM
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the IP Address and Port number
IP = '127.0.0.1'
PORT = 1234

# Connect the client to the server
client.connect((IP, PORT))

# Function to receive messages from the server
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICKNAME':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break

# Function to send messages to the server
def write():
    while True:
        message = input()
        client.send(message.encode('utf-8'))

# Start the receive() and write() functions with threads
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

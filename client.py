import socket
import threading
import random

# Create a server with AF_INET and SOCK_STREAM
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the IP Address and Port number on which the server will run
IP = "127.0.0.1"
PORT = 1234

# Bind the server to the IP and Port with the bind() function
server.bind((IP, PORT))

# Make the server listen to incoming requests with the listen() function
server.listen()

# Create a list of clients to maintain all the clients that connect with the server
clients = []

# Define questions and answers
questions = ["What is the capital of France?", "What is the largest planet in our solar system?"]
answers = ["Paris", "Jupiter"]

# Create a while True loop to accept all the incoming connection requests from the clients with the accept() function
while True:
    # Accept the client's connection request
    client_socket, client_address = server.accept()
    
    # Add the client to the list of clients
    clients.append(client_socket)
    
    # Create a new thread with the Thread() class and add client_thread as the target that takes client socket as an argument. Start the thread
    client_thread = threading.Thread(target=client_thread, args=(client_socket,))
    client_thread.start()

# Create the client_thread() function which will take client socket as an argument
def client_thread(client_socket):
    # Define the client's score. It will be 0 as the game has just started
    score = 0
    
    # Show the client a list of instructions for the game
    instructions = "Welcome to the Quiz Game!\nInstructions:\n1. Answer the questions correctly to earn points.\n2. Each correct answer will earn you 1 point.\n3. Good luck!"
    client_socket.send(instructions.encode('utf-8'))
    
    # Create a function called get_random_question_answer() which will take the client's socket as an argument
    def get_random_question_answer(client_socket):
        # Use the random.randint() method to get a random index from the questions list
        random_index = random.randint(0, len(questions)-1)
        
        # Get the question and its corresponding answer based on the random index
        question = questions[random_index]
        answer = answers[random_index]
        
        # Send the question to the client
        client_socket.send(question.encode('utf-8'))
        
        # Return the random index, question, and answer
        return random_index, question, answer
    
    # Save the returned index, question, and answer in variables in the client_thread() function
    random_index, question, answer = get_random_question_answer(client_socket)
    
    # Create a while True loop in the client_thread() function to listen to any messages received from the client with the recv() function
    while True:
        # Receive the message from the client
        message = client_socket.recv(1024).decode('utf-8')
        
        # Check if the message is a valid message or not
        if not message:
            # If the message is not valid, remove the client from the list of clients
            clients.remove(client_socket)
            break
        
        # Check if the message that the client sent matches with the answer or not
        if message == answer:
            # If the answer matches, add 1 to the client's score
            score += 1
            
            # Send a message to the client that it was the right answer and let them know about their score
            response = f"Correct! Your score is now {score}"
            client_socket.send(response.encode('utf-8'))
            
            # Call the remove_question() function to remove the question and answer at the index
            remove_question(random_index)
            
            # Call the get_random_question_answer() function to get a new set of index, question, and answer for the client
            random_index, question, answer = get_random_question_answer(client_socket)
        else:
            # If the answer was incorrect, send the client a message letting them know that their answer was incorrect
            response = "Incorrect answer. Try again!"
            client_socket.send(response.encode('utf-8'))
            
            # Call the remove_question() function to remove the question and answer at the index
            remove_question(random_index)
            
            # Call the get_random_question_answer() function to get a new set of index, question, and answer for the client
            random_index, question, answer = get_random_question_answer(client_socket)

# Create a function called remove_question() that will take the random index as an argument
def remove_question(random_index):
    # Remove the question and answer at the index in both the questions and answers list
    del questions[random_index]
    del answers[random_index]

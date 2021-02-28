import socket
import secrets
import string
import json
import pickle
import threading
import ctypes
BUFFER_SIZE = 4096

def generate_temp_password(length):

    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password

# Returns True if connected, False otherwise
def connect_chatroom(client, sentence_split): #sentence_split = ["/host", "passwd"]

    #TODO: error checking
    client.send(sentence_split[0].encode()) #send /host or /join
    data = client.recv(BUFFER_SIZE)
    print(data.decode())

    #TODO: Multiserver needs to send a NAK when name exists
    #TODO: error checking
    client.send(sentence_split[1].encode()) #send chatroom_name
    data = client.recv(BUFFER_SIZE)

    if (data.decode() == 'NAK'):
        if(sentence_split[0] == '/host'):
            print('Server name already exists. Please choose another name')
        elif(sentence_split[0] == '/join'):
            print('Chatroom not yet create. Please try again later')
        else:
            #TODO: For testing purposes
            print('Why are you here')
        return False
    else:
        print(data.decode())
        return True

def handle_receive(client):
    while True:
        data = client.recv(BUFFER_SIZE)
        if(data == 0):
            return
        print(data.decode())

#TODO: change to dictionary for faster execution
def in_chatroom(client):
    #Launch thread to receive messages
    recv_thread = threading.Thread(target=handle_receive, args=[client])
    recv_thread.start()

    #Send messages
    while True:
        sentence = input('Input message: ')
    
        # Return to lobby
        if(sentence == '/exit'):
            #TODO: need the server to kill the receiving thread?
            exit()
            recv_thread.join()
            return False
    
        client.send(sentence.encode())


#TODO: change to dictionary for faster execution
def in_lobby(client):
    sentence = input('Use /host [SERVER_NAME] to host a server\n\
Use /join [SERVER_NAME] to join a server\n')

    # Exit program
    if(sentence == '/exit'):
        client.close()
        exit()

    sentence_split = sentence.split()
    #TODO: Discuss how we want to deal with invalid input
    if(len(sentence_split) == 2):
        if(sentence_split[0] == '/host' or sentence_split[0] == '/join'):
            return connect_chatroom(client, sentence_split)
        else:
            print('Invalid input')
            return False
    else:
        print('Invalid input')
        return False


def get_socket():
    # TODO: Hardcoded HOST and PORT

    HOST = '127.0.0.1'
    PORT = 65412

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    return client

def start_chat_client():

    name = input("Name is: " )
    client = get_socket()
    #TODO: error checking
    client.send(name.encode())

    connection_state = False

    while True:
        if(connection_state):
            connection_state = in_chatroom(client)
        else:
            connection_state = in_lobby(client)

def main():
    start_chat_client()

if __name__ == '__main__':
    main()

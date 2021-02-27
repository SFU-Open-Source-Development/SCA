import socket
import secrets
import string
import json
import pickle
import threading
HOST = '127.0.0.1'
PORT = 65412
Size = 4096
HOST_OR_JOIN = False
message_lock = threading.Lock()
def generate_temp_password(length):

    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password

def hostserver(client, sentence_split): #sentence_split = ["/host", "passwd"]
    
    client.send(sentence_split[0].encode()) #send /host
    data = client.recv(Size)
    print( data.decode())
    
    client.send(sentence_split[1].encode()) #send chatroom_name
    data = client.recv(Size)
    print( data.decode())
    

def joinserver(client, sentence_split):
    # f = open('passwd.json')
    # data = json.load(f)
    # client.send(data["name"].encode())
    # data = client.recv(Size)
    # print( data.decode())
    client.send(sentence_split[0].encode()) #send /host
    data = client.recv(Size)
    print( data.decode())
    
    client.send(sentence_split[1].encode()) #send chatroom_name
    data = client.recv(Size)
    if data.decode() == "NAK":
        print("Chatroom not yet created. Please Try later")
        HOST_OR_JOIN = False
        exit()
    print( data.decode())
    print('Received: ', data.decode())
    
def handle_receive(client):
    with message_lock:
        while True:
            data = client.recv(Size)
            print(data.decode())
    
# def checkusers(client, sentence) :
#     client.send(sentence)
#     data = client.recv(Size)
#     print('Received: ', data.decode())

def main():
    # passwd = generate_temp_password(4)
    # print(passwd)
    name = input("Name is: ")
    while True:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        
        data = client.send(name.encode())
        # print(client)
        while True:
            sentence = input('Input Message: ')
            if ((len(sentence.split()) ==2) and (sentence.split()[0] == "/host")):
                
                sentence_split = sentence.split()
                hostserver(client, sentence_split)
                HOST_OR_JOIN = True
                    
                    
            elif ((len(sentence.split()) ==2) and (sentence.split()[0] == "/join")):
                sentence_split = sentence.split()
                joinserver(client, sentence_split)
                HOST_OR_JOIN = True 
   
            # elif sentence_split[0] == "/users":
            #     checkusers(client, sentence)   
                
            elif (HOST_OR_JOIN == True):
                client.send(sentence.encode())
                threading.Thread(target=handle_receive, args=[client]).start()
                
                
                # data = client.recv(Size)
                # print('Received: ', data.decode())
                
            if (sentence == "/exit"):
                client.close()
                exit()
            
if __name__ == '__main__':
    main()
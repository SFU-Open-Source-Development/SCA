from socket import *
import sys
import threading

# list_client = [] # The clients we have connected to
clients_lock = threading.Lock()
dict_client = {}
chatroom = {}
Size = 4096
def createchatroom(data, client, address, name):
    client.send("{} received".format(data).encode()) #/host received
    
    chatroom_name = client.recv(Size).decode() #receive chatroom
    client.send("chatroom_name received {}".format(chatroom_name).encode())
    # chatroom_name = name+str(address[0])
    chatroom[chatroom_name] = {}
    chatroom[chatroom_name]["users"] = [name]
    chatroom[chatroom_name]["Messages"] = []
    chatroom[chatroom_name]["client_address"] = {client}
    return chatroom_name
    # return 0
    
def joinchatroom(data, client, address, name):
    client.send("{} received".format(data).encode()) #/join received
    chatroom_name = client.recv(Size).decode() #receive chatroom
    client.send("chatroom_name received {}".format(chatroom_name).encode())
    
    if chatroom_name in chatroom:
        chatroom[chatroom_name]["users"].append(name)
        chatroom[chatroom_name]["client_address"].add(client)
        print(chatroom)
    else:
        return False
    return chatroom_name

def sendtoAll(chatroom):
    for client in chatroom["client_address"]:
        
        client.send(chatroom["Messages"][-1].encode())
        
        
    
    return 0
    
def handle_client(client, address):
    with clients_lock: #when threading.lock() happens, append client info to list
        # list_client.append(client)
        name = client.recv(Size).decode()
        print(("Hello "+name))
        dict_client[client] = name
        
        
    while True:
        # print(list_client)
        data = client.recv(Size).decode()
        
        # print("Received: {} from Client {}".format(data, dict_client[client]))
        if not data:
            client.send("NAK".encode())
            break
        
        if (data == "/host"):
            result = createchatroom(data, client, address, name)
        # client.send("ACK".encode())
        elif (data == "/join"):
            result = joinchatroom(data, client, address, name)
            if result == False:
                client.send("NAK".encode())
                
            

        elif (data == "/exit"):
            
            print("exiting client {}".format(dict_client[client]))
            del dict_client[client]
            client.close()
            break
        
        else: 
            if chatroom[result]:
               
                message = "{}: {}".format(name, data)
                chatroom[result]["Messages"].append(message)
                # print(chatroom)
                print(chatroom[result]["Messages"][-1])
                sendtoAll(chatroom[result])

            else:
                print("chatroom does not exist")
                client.send("NAK".encode())
                    
                

            # client.close()
            # break
                
        
def main():
    # Run Client1.py and Client2.py and check whether their messages are echoed in Server
    # 
    #
    HOST = '127.0.0.1'
    PORT = 65412
    serverSocket = socket(AF_INET,SOCK_STREAM)
    try:
        serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        serverSocket.bind((HOST, PORT))
    except Exception as e:
        print("Error:Could not bind to port {}. Exiting!".format(PORT))
        sys.exit(1)

    serverSocket.listen(5) #5 for now
    
    print("The server is ready to receive")
    
    while True:
        client, addr = serverSocket.accept()    
        

        threading.Thread(target=handle_client, args=(client, addr)).start()

if __name__ == '__main__':
    main()

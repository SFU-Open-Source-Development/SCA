from socket import *
import sys
import threading

list_client = [] # The clients we have connected to
clients_lock = threading.Lock()
dict_client = {}


def handle_client(client, address):
    with clients_lock: #when threading.lock() happens, append client info to list
        list_client.append(client)
        name = client.recv(1024).decode()
        print(("Hello "+name))
        dict_client[client] = name
        
        
    while True:
        # print(list_client)
        data = client.recv(1024).decode()
        print("Received: {} from Client {}".format(data, dict_client[client]))
        client.send("ACK".encode())
        if not data:
            client.send("NAK".encode())
            break
        elif (data == "/exit"):
            
            print("exiting client {}".format(dict_client[client]))
            del dict_client[client]
            client.close()
            break


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

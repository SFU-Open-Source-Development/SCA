import socket

HOST = '127.0.0.1'
PORT = 65412


while True:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    name = input("Name is: ")
    data = client.send(name.encode())
    # print(client)
    while True:
        sentence = input('Input Message: ')
        client.send(sentence.encode())
        
        data = client.recv(1024)

        print('Received: ', data.decode())
        if (sentence == "/exit"):
            client.close()
            exit()
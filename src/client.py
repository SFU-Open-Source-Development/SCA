import socket

HOST = '127.0.0.1'
PORT = 65412


while True:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print(client)
    while True:
        sentence = input('Input Message: ')
        sentence = str(sentence.split())
        print(sentence)
        client.send(sentence.encode())
        
        data = client.recv(4096)

        print('Received: ', data.decode())
        # client.close()
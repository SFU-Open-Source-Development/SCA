import socket

HOST = '127.0.0.1'
PORT = 65412
while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        sentence = input('Input Message: ')
        client.send(sentence.encode())
        data = client.recv(1024)

        print('Received: ', data.decode())
        client.close()
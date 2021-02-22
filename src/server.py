import socket
import sys


HOST = '127.0.0.1'
PORT = 65412
def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #https://stackoverflow.com/questions/6380057/python-binding-socket-address-already-in-use
            s.bind(('', PORT))
        except:
            print("Error: Could not bind to port {}. Exiting!".format(PORT))
            sys.exit(1)

        print("The server is ready to receive")
        s.listen(1)

        while True:
            conn, addr = s.accept()
            print('Connected by', addr)
            data = conn.recv(1024).decode()
            if not data:
                break
            print("Received: {} from Client".format(data))
            data = data + "123 from Server"
            conn.sendall(data.encode())
          


if __name__ == '__main__':
    main()
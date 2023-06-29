import socket
import threading

HOST = '192.168.99.45'
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()
clients = []
aliases = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    while(True):
        try:
            message=client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat room!'.encode('utf-8'))
            aliases.remove(alias)
            break

def receive():
    while True:
        print('Server is running...')
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)
        print(f'{alias} has connected to the chat room!'.encode('utf-8'))
        broadcast(f'{alias} has connected to the chat room'.encode('utf-8'))
        client.send('you are now connected!'.encode('utf-8'))
        thread = threading.Thread(target = handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    receive()
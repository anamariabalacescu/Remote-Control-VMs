import socket
import threading
import subprocess

HOST = '192.168.203.45'
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()
clients = []
aliases = []

def menu():
    options = [
        "Reseteaza fisier pentru capacitatea memoriei",
        "Reseteaza fisier despre dispozitive hardware",
        "Reseteaza fisier despre dispozitive I/O",
        "Reseteaza fisier despre procese active",
        "Reseteaza fisier despre temperatura",
        "Resetare fisier despre utilizatori si timpi de autentificare",
        "Exit"
    ]

    while True:
        print()
        print("Alege o optiune din meniu:")
        for i, option in enumerate(options, start=1):
            print(f"{i}) {option}")

        choice = input("Optiune: ")
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            choice = int(choice)
            break
        else:
            print("Optiune incorecta!")

    if choice == 1:
        file_name = "storage-unit.txt"
        cmd = 'free -h'
    elif choice == 2:
        file_name = "hw-info.txt"
        cmd = 'hwinfo --short'
    elif choice == 3:
        file_name = "io.txt"
        cmd = 'iostat'
    elif choice == 4:
        file_name = "processes.txt"
        cmd = 'systemctl list-units --type=service --state=running'
    elif choice == 5:
        file_name = "temp.txt"
        cmd = 'sensors'
    elif choice == 6:
        file_name = "login.txt"
        cmd = 'last --since today'
    elif choice == 7:
        print("Goodbye!")
        exit()

    with open("info-ssh.txt", 'r') as info_file:
        for line in info_file:
            acc, ip = line.strip().split()
            with open(file_name, 'a') as file:
                file.write(f"{acc}'s {file_name}:\n")
                subprocess.run(["ssh", f"{acc}@{ip}", cmd], stdout=file)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            aliases.remove(alias)
            break

def receive():
    while True:
        print('Server is running...')
        client, address = server.accept()
        print(f'Connection is established with {str(address)}')
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024).decode('utf-8')
        aliases.append(alias)
        clients.append(client)
        client.send('You are now connected!'.encode('utf-8'))
        menu()
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    receive()


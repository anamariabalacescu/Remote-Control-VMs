import socket

import threading 



IP = '192.168.1.139'

#socket.gethostbyname(socket.gethostname())

PORT = 9090

ADDR = (IP, PORT)

SIZE = 1024

FORMAT = "utf-8"

DISCONNECT_MSG = "!DISCONNECT"



def menu():
    options = [
        "Reseteaza fisier pentru capacitatea memoriei",
        "Reseteaza fisier despre dispozitive hardware",
        "Reseteaza fisier despre dispozitive I/O",
        "Reseteaza fisier despre procese active",
        "Reseteaza fisier despre temperatura",
        "Resetare fisier despre utilizatori si timpi de autentificare","Exit"]
    while 1:
        print("Alege o optiune din meniu:")
        for i,option in enumerate(options):
            print("{1}. Select {2}".format(i,option))


        choice = input("Optiune: ")

        if choice.isdigit() and 1 <= int(choice) <= len(options):
            choice = int(choice)
            break
        else:
            print("Optiune incorecta!")
        
        if choice == 1:
            print("1")
            file_name = "storage-unit.txt"
            cmd = 'free -h'
        elif choice == 2:
            print("2")
            file_name = "hw-info.txt"
            cmd = 'hwinfo --short'
        elif choice == 3:
            print("3")
            file_name = "io.txt"
            cmd = 'iostat'
        elif choice == 4:
            print("4")
            file_name = "processes.txt"
            cmd = 'systemctl list-units --type=service --state=running'
        elif choice == 5:
            print("5")
            file_name = "temp.txt"
            cmd = 'sensors'
        elif choice == 6:
            print("6")
            file_name = "login.txt"
            cmd = 'last --since today'
        elif choice == 7:
            print("Goodbye!")
            exit()





def handle_client(conn, addr):

	print(f"[NEW CONNECTION] {addr} connected.")

	

	connected = True

	while connected:

		msg = conn.recv(SIZE).decode(FORMAT)
  
		

		if msg == DISCONNECT_MSG:

			connected = False

		

		print(f"[{addr}]{msg}")

		conn.send(msg.encode(FORMAT))

	

	conn.close()



def main():

	print("[STARTING] Server is strating ... ")

	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	server.bind(ADDR)

	server.listen()

	print(f"[LISTENING] Server is listening on {IP}:{PORT}")

	

	while True:

		conn, addr = server.accept()

		thread =  threading.Thread(target=handle_client, args=(conn, addr))

		thread.start()

		print(f"[ACTIVE CONNECTIONS] {threading.active_count() -1}")

		

if __name__ == "__main__":

	main()


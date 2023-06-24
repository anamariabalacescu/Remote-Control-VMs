import socket
import subprocess
import threading 
import paramiko
import os
from paramiko import SSHConfig
import curses
import datetime


IP = '192.168.83.45'

IP_CL = None

USER_CL = None

#socket.gethostbyname(socket.gethostname())

PORT = 9090

ADDR = (IP, PORT)

SIZE = 1024

FORMAT = "utf-8"

DISCONNECT_MSG = "!DISCONNECT"

stop_event = threading.Event()

def create_client_folder(client_name):
    folder_name = f"clients/{client_name}"  # Assuming the folder is created within a 'clients' directory

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Folder '{folder_name}' created.")
    else:
        print(f"Folder '{folder_name}' already exists.")

def reset_files():
    files = ["storage-unit.txt", "hw-info.txt", "io.txt", "processes.txt", "temp.txt", "login.txt", "system.txt"]
    for file in files:
        subprocess.run(["truncate", "-s", "0", file])

def get_private_key_path():
    default_private_key_path = os.path.expanduser("~/.ssh/id_rsa")
    
    if os.path.isfile(default_private_key_path):
        return default_private_key_path
    else:
        return None

def execute_ssh_command(cmd):
    private_key_path = get_private_key_path()
    if private_key_path is None:
        print("Private key path not found.")
        return None
    
    ssh_command = f"ssh -i {private_key_path} {USER_CL}@{IP_CL} \"{cmd}\""
    output = subprocess.check_output(ssh_command, stderr=subprocess.STDOUT, shell=True).decode(FORMAT)

    return output.strip()

def send_public_key(conn, username):
    public_key_path = os.path.expanduser("~/.ssh/id_rsa.pub")
    if os.path.isfile(public_key_path):
        with open(public_key_path, "r") as file:
            public_key = file.read().strip()
            server_info = f"{username},{public_key}"
            conn.send(server_info.encode(FORMAT))
            print("Public key - sent.")
    else:
        print("Public key- NOT sent.")
	#subprocess.run(["ssh-keygen", "-t", "rsa", "-f", "id_rsa", "-N", ""], capture_output=True)
	#subprocess.run(["ssh-copy-id", "-i", "id_rsa.pub", f"{IP_CL}"])
    #server_info = f"{myname}, {pub_key}"
	#server.send(server_info.encode(FORMAT))

def stop_service(output):
	stdscr = curses.initscr()
	curses.cbreak()
	stdscr.keypad(True)
    
	stdscr.clear()
    
	stdscr.addstr("\nActive services:\n")
	stdscr.addstr("output")
	
	stdscr.addstr("\nPress any key to continue...")
	stdscr.refresh()

	stdscr.getch()
	stdscr.refresh()
	stdscr.getch()
    
	curses.nocbreak()
	stdscr.keypad(False)
	curses.echo()
	curses.endwin()

def opt1_s_submenu(conn, adr):
    options = ["Oprire Servicii", "Pornire Servicii", "Restartare Servicii"]
    stdscr = curses.initscr()
    selected_option = 0
    curses.cbreak()
    stdscr.keypad(True)
    
    while True:
        stdscr.clear()
        
        for i, option in enumerate(options):
            if i == selected_option:
                stdscr.addstr(f"-> {option}\n")
            else:
                stdscr.addstr(f"    {option}\n")
        
        stdscr.refresh()
        
        key = stdscr.getch()
        
        if key == curses.KEY_UP:
            selected_option = (selected_option - 1) % len(options)
        elif key == curses.KEY_DOWN:
            selected_option = (selected_option + 1) % len(options)
        elif key == ord('\n'):
            chosen_option = options [selected_option]
            stdscr.addstr(f"\nYou selected: {chosen_option}\n")
            stdscr.addstr(f"\nPress -> to go further\n")
            stdscr.refresh()
            
            stdscr.getch()
            if chosen_option == "Oprire Servicii":
                cmd = f"systemctl list-units --type=service --state=running --no-pager | head -n -4 | tail -n +2 "
                output = execute_ssh_command(cmd)
                if output:
                    stop_service(output)
                else:
                    stdscr.addstr("\nNo active services found.\n")
        elif key == 27: #ESC
            break
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

def opt1(conn, addr):
    options = ["Servicii", "Procese"]
    stdscr = curses.initscr()
    selected_option = 0
    curses.cbreak()
    stdscr.keypad(True)
    
    while True:
        stdscr.clear()
        
        for i, option in enumerate(options):
            if i == selected_option:
                stdscr.addstr(f"-> {option}\n")
            else:
                stdscr.addstr(f"    {option}\n")
        
        stdscr.refresh()
        
        key = stdscr.getch()
        
        if key == curses.KEY_UP:
            selected_option = (selected_option - 1) % len(options)
        elif key == curses.KEY_DOWN:
            selected_option = (selected_option + 1) % len(options)
        elif key == ord('\n'):
            chosen_option = options [selected_option]
            stdscr.addstr(f"\nYou selected: {chosen_option}\n")
            stdscr.addstr(f"\nPress -> to go further\n")
            stdscr.refresh()
            
            stdscr.getch()
            if chosen_option == "Servicii":
                opt1_s_submenu(conn, addr)
        elif key == 27: #ESC
            break
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    
def opt3(conn, addr):
    options = ["Aplicatii", "Servicii"]
    stdscr = curses.initscr()
    curses.cbreak()
    stdscr.keypad(True)
    
    while True:
        stdscr.clear()
        
        for i, option in enumerate(options):
            if i == selected_option:
                stdscr.addstr(f"-> {option}\n")
            else:
                stdscr.addstr(f"    {option}\n")
        
        stdscr.refresh()
        
        key = stdscr.getch()
        
        if key == curses.KEY_UP:
            selected_option = (selected_option - 1) % len(options)
        elif key == curses.KEY_DOWN:
            selected_option = (selected_option + 1) % len(options)
        elif key == ord('\n'):
            chosen_option = options [selected_option]
            stdscr.addstr(f"\nYou selected: {chosen_option}\n")
            stdscr.addstr(f"\nPress -> to go further\n")
            stdscr.refresh()
            
            stdscr.getch()
        elif key == 27: #ESC
            break
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

def menu(conn, addr):
    options = ["Oprire/pornire servicii/procese", "Copiere fisiere", "Instalare aplicatii/servicii"]
    selected_option = 0
    
    stdscr = curses.initscr()
    curses.cbreak()
    stdscr.keypad(True)
    
    while True:
        stdscr.clear()
        stdscr.addstr("Menu:\n")
        
        for i, option in enumerate(options):
            if i == selected_option:
                stdscr.addstr(f"-> {option}\n")
            else:
                stdscr.addstr(f"    {option}\n")
        
        stdscr.refresh()
        
        key = stdscr.getch()
        
        if key == curses.KEY_UP:
            selected_option = (selected_option - 1) % len(options)
        elif key == curses.KEY_DOWN:
            selected_option = (selected_option + 1) % len(options)
        elif key == ord('\n'):
            chosen_option = options [selected_option]
            stdscr.addstr(f"\nYou selected: {chosen_option}\n")
            stdscr.addstr(f"\nPress -> to go further\n")
            stdscr.refresh()
            stdscr.getch()
            if chosen_option == "Oprire/pornire servicii/procese":
                opt1(conn, addr)
            elif chosen_option == "Instalare aplicatii/servicii":
                opt3(conn, addr)

        elif key == 27: #ESC
            break
       
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

def handle_client(conn, addr):

	print(f"[NEW CONNECTION] {addr} connected.")

	data = conn.recv(SIZE).decode(FORMAT)

	username, client_ip = data.split(",")
    
	global IP_CL
	IP_CL = client_ip

	global USER_CL
	USER_CL = username

	with open("info-shh.txt", "a") as file:

		file.write(f"{username} {client_ip}")
    
	user = subprocess.check_output("whoami").decode().strip()
	send_public_key(conn, user)
    
	while True:#not stop_event.is_set():

		options = [
			("Reseteaza fisier pentru capacitatea memoriei","storage-unit.txt", "free -h"),
            ("Reseteaza fisier despre dispozitive hardware","hw-info.txt", "hwinfo --short"),
            ("Reseteaza fisier despre dispozitive I/O","io.txt", "iostat"),
            ("Reseteaza fisier despre procese active","processes.txt", "systemctl list-units --type=service --state=running"),
            ("Reseteaza fisier despre temperatura","temp.txt", "sensors"),
            ("Resetare fisier despre utilizatori si timpi de autentificare","login.txt", "last --since today"),
			("Reseteaza fisier pentru informatii de sistem","system.txt", "neofetch | tail -n 18")
        ]

		for option in options:
			menu_title, file_name, cmd = option
			output = execute_ssh_command(cmd)
			if output is not None:
				#print("[CLIENT] Command output:\n{output}")
				with open(file_name, "a") as file:
					file.write(f"\nData: {datetime.datetime.now()}\n")
					file.write(f"{username}'s info:")
					file.write(output)
					file.write(f"\n")
			#else:
				#print("[CLIENT] Failed to execute command: {cmd}")
    #threading.Timer(300, menu, args=(conn, addr)).start()
	
	threading.Event().wait(300)    
	#stop_event.wait(300)
 
	conn.close()



def main():

	print("[STARTING] Server is strating ... ")

	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	server.bind(ADDR)

	server.listen()

	print(f"[LISTENING] Server is listening on {IP}:{PORT}")

	

	while True:

		conn, addr = server.accept()

		#ssh_public_key = open("~/.ssh/id_rsa.pub").read().encode(FORMAT)
        
		thread =  threading.Thread(target=handle_client, args=(conn, addr))

		thread.start()

		menu_thread = threading.Thread(target=menu, args=(conn, addr))
		menu_thread.start()

        #stop_event.set()
        
        #for thread in threads:
        #    thread.join()
        

		print(f"[ACTIVE CONNECTIONS] {threading.active_count() -1}")

reset_files	

if __name__ == "__main__":

	main()
#menu()


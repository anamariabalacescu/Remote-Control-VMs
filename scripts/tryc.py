import socket
import subprocess

IP = '192.168.1.139'
PORT = 9090
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

def send_ssh_key():
	subprocess.run(["ssh-keygen", "-t", "rsa", "-f", "id_rsa"], capture_output=True)
	subprocess.run(["ssh-copy-id", "-i", "id_rsa.pub", f"{IP}"])

def main():
	
	send_ssh_key()

	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect(ADDR)
	print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")

	print("Done")

	username = subprocess.check_output("whoami").decode().strip()
	client_ip = socket.gethostbyname(socket.getfqdn())
	#client_ip = socket.gethostbyname(socket.gethostname())
	ssh_public_key = open("id_rsa.pub").read()
	client_info = f"{username},{client_ip},{ssh_public_key}"
	client.send(client_info.encode(FORMAT))

	connected = True
	while connected:
		msg = input("> ")
		
		if msg == DISCONNECT_MSG:
			connected = False
		else:
			msg = client.recv(SIZE).decode(FORMAT)
			print(f"[SERVER] {msg}")
	
if __name__ == "__main__":
	main()	

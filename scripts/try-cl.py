import socket

IP = '192.168.99.45'
PORT = 9090
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

def main():
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect(ADDR)
	print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")
	
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

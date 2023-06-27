import socket
import subprocess
import threading 
import paramiko
import os
from paramiko import SSHConfig
import curses
import datetime
import time
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import re

IP = '192.168.1.135'
IP_CL = None
USER_CL = None
PORT = 9090
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

def create_client_folder(client_name):
	folder_name = f"clients/{client_name}"  

	if not os.path.exists(folder_name):
		os.makedirs(folder_name)
		print(f"Folder '{folder_name}' created.")
	else:
		print(f"Folder '{folder_name}' already exists.")

def reset_files():
	files = ["storage-unit.txt", "hw-info.txt", "io.txt", "processes.txt", "temp.txt", "login.txt", "system.txt"]
	for file in files:
		subprocess.run(["touch", file])
		with open(file, "w") as f:
			f.truncate(0)
		
def create_files():
	files = ["storage-unit.txt", "hw-info.txt", "io.txt", "processes.txt", "temp.txt", "login.txt", "system.txt"]
	for file in files:
		subprocess.run(["touch", file])
		with open(file, "w") as f:
			f.truncate(0)

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
			#print("Public key - sent.")
	else:
		print("Public key- NOT sent.")

def try_again(conn, addr):
	def go_back():
		failmeniu.destroy()
		menu(conn,addr)
        
	def exit_prg():
		failmeniu.destroy()
		exit()
		
	failmeniu = tk.Tk()
	failmeniu.title("Executed!")
	failmeniu.geometry("500x500")
 
	image = Image.open("/home/student/project-2023/stitch-read.jpg")
	image = image.resize((500, 500), Image.ANTIALIAS)
	background_image = ImageTk.PhotoImage(image)

	background_label = tk.Label(failmeniu, image=background_image)
	background_label.place(x=0, y=0, relwidth=1, relheight=1)

	style = ttk.Style(failmeniu)
	style.configure("TFrame", background="#b3c6e7")
	style.configure("TButton", background="#441f8a", foreground="#ffffff", font=("Arial", 12, "bold"))
	style.configure("TLabel", background="#b3c8e7", foreground="#000000", font=("Arial", 12))
	style.configure("TCombobox", background="#324ba9", foreground="#ffffff", font=("Arial", 12))

	frame = ttk.Frame(failmeniu, style = "TFrame")
	frame.pack(padx=20, pady=20)
    
	label = ttk.Label(frame, text="Well done! Command executed succefully!", style="TLabel")
	label.grid(row=0, column=0, padx=10, pady=10)
    
	exit_button = ttk.Button(frame, text="Exit", command=exit_prg, style="TButton")
	exit_button.grid(row=1, column=0,  padx=30, pady=30)

	back_button = ttk.Button(frame, text="Back", command=go_back, style="TButton")
	back_button.grid(row=1, column=1,  padx=30, pady=30)
    
	failmeniu.mainloop()

def good_job(conn, addr):
	def go_back():
		gjmeniu.destroy()
		menu(conn,addr)
        
	def exit_prg():
		gjmeniu.destroy()
		exit()
		
	gjmeniu = tk.Tk()
	gjmeniu.title("Executed!")
	gjmeniu.geometry("500x500")
 
	image = Image.open("/home/student/project-2023/stitch-congrats.jpg")
	image = image.resize((500, 500), Image.ANTIALIAS)
	background_image = ImageTk.PhotoImage(image)

	background_label = tk.Label(gjmeniu, image=background_image)
	background_label.place(x=0, y=0, relwidth=1, relheight=1)

	style = ttk.Style(gjmeniu)
	style.configure("TFrame", background="#b3c6e7")
	style.configure("TButton", background="#441f8a", foreground="#ffffff", font=("Arial", 12, "bold"))
	style.configure("TLabel", background="#b3c8e7", foreground="#000000", font=("Arial", 12))
	style.configure("TCombobox", background="#324ba9", foreground="#ffffff", font=("Arial", 12))

	frame = ttk.Frame(gjmeniu, style = "TFrame")
	frame.pack(padx=20, pady=20)
    
	label = ttk.Label(frame, text="Well done! Command executed succefully!", style="TLabel")
	label.grid(row=0, column=0, padx=10, pady=10)
    
	exit_button = ttk.Button(frame, text="Exit", command=exit_prg, style="TButton")
	exit_button.grid(row=1, column=0,  padx=30, pady=30)

	back_button = ttk.Button(frame, text="Back", command=go_back, style="TButton")
	back_button.grid(row=1, column=1,  padx=30, pady=30)
    
	gjmeniu.mainloop()

def stop_service(conn, addr):
	def go_back():
		ssmeniu.destroy()
		opt1_s_submenu(conn,addr)
        
	def select_option():
		chosen_option = options_box.get()
		ssmeniu.destroy()
		good_job(conn, addr)
		
	cmd = f"systemctl list-units --type=service --state=running --no-pager | head -n -4 | tail -n +2 | cut -d ' ' -f3"
	output = execute_ssh_command(cmd)
	options = output.split('\n')
	ssmeniu = tk.Tk()
	ssmeniu.title("Oprire Servicii")
	ssmeniu.geometry("500x500")
 
	image = Image.open("/home/student/project-2023/stitch-read.jpg")
	image = image.resize((500, 500), Image.ANTIALIAS)
	background_image = ImageTk.PhotoImage(image)

	background_label = tk.Label(ssmeniu, image=background_image)
	background_label.place(x=0, y=0, relwidth=1, relheight=1)

	style = ttk.Style(ssmeniu)
	style.configure("TFrame", background="#b3c6e7")
	style.configure("TButton", background="#441f8a", foreground="#ffffff", font=("Arial", 12, "bold"))
	style.configure("TLabel", background="#b3c8e7", foreground="#000000", font=("Arial", 12))
	style.configure("TCombobox", background="#324ba9", foreground="#ffffff", font=("Arial", 12))

	frame = ttk.Frame(ssmeniu, style = "TFrame")
	frame.pack(padx=20, pady=20)
    
	label = ttk.Label(frame, text="Select an option:", style="TLabel")
	label.grid(row=0, column=0, padx=10, pady=10)
    
	options_box = ttk.Combobox(frame, values=options, font=("Arial", 12), state="readonly", style = "TCombobox")
	options_box.grid(row=0, column=1, padx=10, pady=10)
	options_box.current(0)
    
	select_button = ttk.Button(frame, text="Select", command=select_option, style="TButton")
	select_button.grid(row=1, column=0,  padx=30, pady=30)

	back_button = ttk.Button(frame, text="Back", command=go_back, style="TButton")
	back_button.grid(row=1, column=1,  padx=30, pady=30)
    
	ssmeniu.mainloop()
        
def start_service(conn, addr):
	def go_back():
		ssmeniu.destroy()
		opt1_s_submenu(conn,addr)
        
	def select_option():
		chosen_option = options_box.get()
		ssmeniu.destroy()
		good_job()
		
	cmd = f"systemctl list-units --type=service --state=inactive --no-pager | head -n -6 | tail -n +2 | sed 's/^[^a-zA-Z]//g' | cut -d ' ' -f2"
	output = execute_ssh_command(cmd)
	options = output.split('\n')
	ssmeniu = tk.Tk()
	ssmeniu.title("Oprire Servicii")
	ssmeniu.geometry("500x500")
 
	image = Image.open("/home/student/project-2023/stitch-read.jpg")
	image = image.resize((500, 500), Image.ANTIALIAS)
	background_image = ImageTk.PhotoImage(image)

	background_label = tk.Label(ssmeniu, image=background_image)
	background_label.place(x=0, y=0, relwidth=1, relheight=1)

	style = ttk.Style(ssmeniu)
	style.configure("TFrame", background="#b3c6e7")
	style.configure("TButton", background="#441f8a", foreground="#ffffff", font=("Arial", 12, "bold"))
	style.configure("TLabel", background="#b3c8e7", foreground="#000000", font=("Arial", 12))
	style.configure("TCombobox", background="#324ba9", foreground="#ffffff", font=("Arial", 12))

	frame = ttk.Frame(ssmeniu, style = "TFrame")
	frame.pack(padx=20, pady=20)
    
	label = ttk.Label(frame, text="Select an option:", style="TLabel")
	label.grid(row=0, column=0, padx=10, pady=10)
    
	options_box = ttk.Combobox(frame, values=options, font=("Arial", 12), state="readonly", style = "TCombobox")
	options_box.grid(row=0, column=1, padx=10, pady=10)
	options_box.current(0)
    
	select_button = ttk.Button(frame, text="Select", command=select_option, style="TButton")
	select_button.grid(row=1, column=0,  padx=30, pady=30)

	back_button = ttk.Button(frame, text="Back", command=go_back, style="TButton")
	back_button.grid(row=1, column=1,  padx=30, pady=30)
    
	ssmeniu.mainloop()


def restart_service(conn, addr):
	def go_back():
		ssmeniu.destroy()
		opt1_s_submenu(conn,addr)
        
	def select_option():
		chosen_option = options_box.get()
		
	cmd = f"systemctl list-units --type=service --state=running --no-pager | head -n -4 | tail -n +2 | cut -d ' ' -f3"
	output = execute_ssh_command(cmd)
	options = output.split('\n')
	ssmeniu = tk.Tk()
	ssmeniu.title("Oprire Servicii")
	ssmeniu.geometry("500x500")
 
	image = Image.open("/home/student/project-2023/stitch-read.jpg")
	image = image.resize((500, 500), Image.ANTIALIAS)
	background_image = ImageTk.PhotoImage(image)

	background_label = tk.Label(ssmeniu, image=background_image)
	background_label.place(x=0, y=0, relwidth=1, relheight=1)

	style = ttk.Style(ssmeniu)
	style.configure("TFrame", background="#b3c6e7")
	style.configure("TButton", background="#441f8a", foreground="#ffffff", font=("Arial", 12, "bold"))
	style.configure("TLabel", background="#b3c8e7", foreground="#000000", font=("Arial", 12))
	style.configure("TCombobox", background="#324ba9", foreground="#ffffff", font=("Arial", 12))

	frame = ttk.Frame(ssmeniu, style = "TFrame")
	frame.pack(padx=20, pady=20)
    
	label = ttk.Label(frame, text="Select an option:", style="TLabel")
	label.grid(row=0, column=0, padx=10, pady=10)
    
	options_box = ttk.Combobox(frame, values=options, font=("Arial", 12), state="readonly", style = "TCombobox")
	options_box.grid(row=0, column=1, padx=10, pady=10)
	options_box.current(0)
    
	select_button = ttk.Button(frame, text="Select", command=select_option, style="TButton")
	select_button.grid(row=1, column=0,  padx=30, pady=30)

	back_button = ttk.Button(frame, text="Back", command=go_back, style="TButton")
	back_button.grid(row=1, column=1,  padx=30, pady=30)
    
	ssmeniu.mainloop()

def opt1_s_submenu(conn, addr):
	def go_back():
		ssmeniu.destroy()
		opt1(conn,addr)
        
	def select_option():
		chosen_option = options_box.get()
		ssmeniu.destroy()
		if chosen_option == "Oprire Servicii":
			stop_service(conn, addr)
		elif chosen_option == "Pornire Servicii":
			start_service(conn, addr)
		elif chosen_option == "Resetare Servicii":
			restart_service(conn, addr)
	
	options = ["Oprire Servicii", "Pornire Servicii", "Restartare Servicii"]
	ssmeniu = tk.Tk()
	ssmeniu.title("Actiune pe Servicii")
	ssmeniu.geometry("500x500")
 
	image = Image.open("/home/student/project-2023/stitch-read.jpg")
	image = image.resize((500, 500), Image.ANTIALIAS)
	background_image = ImageTk.PhotoImage(image)

	background_label = tk.Label(ssmeniu, image=background_image)
	background_label.place(x=0, y=0, relwidth=1, relheight=1)

	style = ttk.Style(ssmeniu)
	style.configure("TFrame", background="#b3c6e7")
	style.configure("TButton", background="#441f8a", foreground="#ffffff", font=("Arial", 12, "bold"))
	style.configure("TLabel", background="#b3c8e7", foreground="#000000", font=("Arial", 12))
	style.configure("TCombobox", background="#324ba9", foreground="#ffffff", font=("Arial", 12))

	frame = ttk.Frame(ssmeniu, style = "TFrame")
	frame.pack(padx=20, pady=20)
    
	label = ttk.Label(frame, text="Select an option:", style="TLabel")
	label.grid(row=0, column=0, padx=10, pady=10)
    
	options_box = ttk.Combobox(frame, values=options, font=("Arial", 12), state="readonly", style = "TCombobox")
	options_box.grid(row=0, column=1, padx=10, pady=10)
	options_box.current(0)
    
	select_button = ttk.Button(frame, text="Select", command=select_option, style="TButton")
	select_button.grid(row=1, column=0,  padx=30, pady=30)

	back_button = ttk.Button(frame, text="Back", command=go_back, style="TButton")
	back_button.grid(row=1, column=1,  padx=30, pady=30)
 
	ssmeniu.mainloop()

def stop_process(conn, addr):
	def go_back():
		ssmeniu.destroy()
		opt1_s_submenu(conn,addr)
        
	def select_option():
		chosen_option = options_box.get()
		
	cmd = f"top -b -n 1 | sed '1,7d' | grep ' R ' | rev | cut -d ' ' -f1 | rev  --procese active"
	output = execute_ssh_command(cmd)
	options = output.split('\n')
	ssmeniu = tk.Tk()
	ssmeniu.title("Oprire Servicii")
	ssmeniu.geometry("500x500")
 
	image = Image.open("/home/student/project-2023/stitch-read.jpg")
	image = image.resize((500, 500), Image.ANTIALIAS)
	background_image = ImageTk.PhotoImage(image)

	background_label = tk.Label(ssmeniu, image=background_image)
	background_label.place(x=0, y=0, relwidth=1, relheight=1)

	style = ttk.Style(ssmeniu)
	style.configure("TFrame", background="#b3c6e7")
	style.configure("TButton", background="#441f8a", foreground="#ffffff", font=("Arial", 12, "bold"))
	style.configure("TLabel", background="#b3c8e7", foreground="#000000", font=("Arial", 12))
	style.configure("TCombobox", background="#324ba9", foreground="#ffffff", font=("Arial", 12))

	frame = ttk.Frame(ssmeniu, style = "TFrame")
	frame.pack(padx=20, pady=20)
    
	label = ttk.Label(frame, text="Select an option:", style="TLabel")
	label.grid(row=0, column=0, padx=10, pady=10)
    
	options_box = ttk.Combobox(frame, values=options, font=("Arial", 12), state="readonly", style = "TCombobox")
	options_box.grid(row=0, column=1, padx=10, pady=10)
	options_box.current(0)
    
	select_button = ttk.Button(frame, text="Select", command=select_option, style="TButton")
	select_button.grid(row=1, column=0,  padx=30, pady=30)

	back_button = ttk.Button(frame, text="Back", command=go_back, style="TButton")
	back_button.grid(row=1, column=1,  padx=30, pady=30)
    
	ssmeniu.mainloop()
        
def start_process(conn, addr):
	def go_back():
		ssmeniu.destroy()
		opt1_s_submenu(conn,addr)
        
	def select_option():
		chosen_option = options_box.get()
		
	cmd = f"top -b -n 1 | sed '1,7d' | grep -v ' R ' | rev | cut -d ' ' -f1 | rev"
	output = execute_ssh_command(cmd)
	options = output.split('\n')
	ssmeniu = tk.Tk()
	ssmeniu.title("Oprire Servicii")
	ssmeniu.geometry("500x500")
 
	image = Image.open("/home/student/project-2023/stitch-read.jpg")
	image = image.resize((500, 500), Image.ANTIALIAS)
	background_image = ImageTk.PhotoImage(image)

	background_label = tk.Label(ssmeniu, image=background_image)
	background_label.place(x=0, y=0, relwidth=1, relheight=1)

	style = ttk.Style(ssmeniu)
	style.configure("TFrame", background="#b3c6e7")
	style.configure("TButton", background="#441f8a", foreground="#ffffff", font=("Arial", 12, "bold"))
	style.configure("TLabel", background="#b3c8e7", foreground="#000000", font=("Arial", 12))
	style.configure("TCombobox", background="#324ba9", foreground="#ffffff", font=("Arial", 12))

	frame = ttk.Frame(ssmeniu, style = "TFrame")
	frame.pack(padx=20, pady=20)
    
	label = ttk.Label(frame, text="Select an option:", style="TLabel")
	label.grid(row=0, column=0, padx=10, pady=10)
    
	options_box = ttk.Combobox(frame, values=options, font=("Arial", 12), state="readonly", style = "TCombobox")
	options_box.grid(row=0, column=1, padx=10, pady=10)
	options_box.current(0)
    
	select_button = ttk.Button(frame, text="Select", command=select_option, style="TButton")
	select_button.grid(row=1, column=0,  padx=30, pady=30)

	back_button = ttk.Button(frame, text="Back", command=go_back, style="TButton")
	back_button.grid(row=1, column=1,  padx=30, pady=30)
    
	ssmeniu.mainloop()

def opt1_p_submenu(conn, addr):
	def go_back():
		ssmeniu.destroy()
		opt1(conn,addr)
        
	def select_option():
		chosen_option = options_box.get()
		ssmeniu.destroy()
		if chosen_option == "Oprire Procese":
			stop_process(conn, addr)
		elif chosen_option == "Pornire Procese":
			start_process(conn, addr)
	
	options = ["Oprire Procese", "Pornire Procese"]
	ssmeniu = tk.Tk()
	ssmeniu.title("Actiune pe Procese")
	ssmeniu.geometry("500x500")
 
	image = Image.open("/home/student/project-2023/stitch-bookes.jpg")
	image = image.resize((500, 500), Image.ANTIALIAS)
	background_image = ImageTk.PhotoImage(image)

	background_label = tk.Label(ssmeniu, image=background_image)
	background_label.place(x=0, y=0, relwidth=1, relheight=1)

	style = ttk.Style(ssmeniu)
	style.configure("TFrame", background="#b3c6e7")
	style.configure("TButton", background="#441f8a", foreground="#ffffff", font=("Arial", 12, "bold"))
	style.configure("TLabel", background="#b3c8e7", foreground="#000000", font=("Arial", 12))
	style.configure("TCombobox", background="#324ba9", foreground="#ffffff", font=("Arial", 12))

	frame = ttk.Frame(ssmeniu, style = "TFrame")
	frame.pack(padx=20, pady=20)
    
	label = ttk.Label(frame, text="Select an option:", style="TLabel")
	label.grid(row=0, column=0, padx=10, pady=10)
    
	options_box = ttk.Combobox(frame, values=options, font=("Arial", 12), state="readonly", style = "TCombobox")
	options_box.grid(row=0, column=1, padx=10, pady=10)
	options_box.current(0)
    
	select_button = ttk.Button(frame, text="Select", command=select_option, style="TButton")
	select_button.grid(row=1, column=0,  padx=30, pady=30)

	back_button = ttk.Button(frame, text="Back", command=go_back, style="TButton")
	back_button.grid(row=1, column=1,  padx=30, pady=30)
 
	ssmeniu.mainloop()


def opt1(conn, addr):
	def go_back():
		sub_meniu.destroy()
		menu(conn,addr)
        
	def select_option():
		chosen_option = options_box.get()
		sub_meniu.destroy()
		if chosen_option == "Servicii":
			opt1_s_submenu(conn, addr)
		elif chosen_option == "Procese":
			opt1_p_submenu(conn, addr)
   
	options = ["Servicii", "Procese"]
	sub_meniu = tk.Tk()
	sub_meniu.title("Actiune pe servicii/procese")
	sub_meniu.geometry("500x500")

	image = Image.open("/home/student/project-2023/stitch-work.jpg")
	image = image.resize((500, 500), Image.ANTIALIAS)
	background_image = ImageTk.PhotoImage(image)

	background_label = tk.Label(sub_meniu, image=background_image)
	background_label.place(x=0, y=0, relwidth=1, relheight=1)

	style = ttk.Style(sub_meniu)
	style.configure("TFrame", background="#b3c6e7")
	style.configure("TButton", background="#441f8a", foreground="#ffffff", font=("Arial", 12, "bold"))
	style.configure("TLabel", background="#b3c8e7", foreground="#000000", font=("Arial", 12))
	style.configure("TCombobox", background="#324ba9", foreground="#ffffff", font=("Arial", 12))

	frame = ttk.Frame(sub_meniu, style = "TFrame")
	frame.pack(padx=20, pady=20)
    
	label = ttk.Label(frame, text="Select an option:", style="TLabel")
	label.grid(row=0, column=0, padx=10, pady=10)
    
	options_box = ttk.Combobox(frame, values=options, font=("Arial", 12), state="readonly", style = "TCombobox")
	options_box.grid(row=0, column=1, padx=10, pady=10)
	options_box.current(0)
    
	select_button = ttk.Button(frame, text="Select", command=select_option, style="TButton")
	select_button.grid(row=1, column=0,  padx=30, pady=30)

	back_button = ttk.Button(frame, text="Back", command=go_back, style="TButton")
	back_button.grid(row=1, column=1,  padx=30, pady=30)
    
	sub_meniu.mainloop()

def opt2(conn, addr):
	def go_back():
		submeniu.destroy()
		menu(conn,addr)
  
	def select_option():
		chosen_option = options_box.get()
		
	cmd = f"find . -type f"
	output = execute_ssh_command(cmd)
	options = output.split('\n')
	submeniu = tk.Tk()
	submeniu.title("Oprire Servicii")
	submeniu.geometry("500x500")
 
	image = Image.open("/home/student/project-2023/stitch-read.jpg")
	image = image.resize((500, 500), Image.ANTIALIAS)
	background_image = ImageTk.PhotoImage(image)

	background_label = tk.Label(submeniu, image=background_image)
	background_label.place(x=0, y=0, relwidth=1, relheight=1)

	style = ttk.Style(submeniu)
	style.configure("TFrame", background="#b3c6e7")
	style.configure("TButton", background="#441f8a", foreground="#ffffff", font=("Arial", 12, "bold"))
	style.configure("TLabel", background="#b3c8e7", foreground="#000000", font=("Arial", 12))
	style.configure("TCombobox", background="#324ba9", foreground="#ffffff", font=("Arial", 12))

	frame = ttk.Frame(submeniu, style = "TFrame")
	frame.pack(padx=20, pady=20)
    
	label = ttk.Label(frame, text="Select an option:", style="TLabel")
	label.grid(row=0, column=0, padx=10, pady=10)
    
	options_box = ttk.Combobox(frame, values=options, font=("Arial", 12), state="readonly", style = "TCombobox")
	options_box.grid(row=0, column=1, padx=10, pady=10)
	options_box.current(0)
    
	select_button = ttk.Button(frame, text="Select", command=select_option, style="TButton")
	select_button.grid(row=1, column=0,  padx=30, pady=30)

	back_button = ttk.Button(frame, text="Back", command=go_back, style="TButton")
	back_button.grid(row=1, column=1,  padx=30, pady=30)

	submeniu.mainloop()

def opt3(conn, addr):
	def go_back():
		sub_meniu.destroy()
		menu(conn,addr)
        
	def select_option():
		chosen_option = input_box.get()
		if system_type == "debian":
			cmd = f"sudo apt-get install {input_box}"
		elif system_type == "Red Hat":
			cmd = f"sudo yum install {input_box}"
		elif system_type == "openSSUE":
			cmd = f"sudo zypper install {input_box}"
		elif system_type == "Arch":
			cmd = f"sudo pacman -S {input_box}"
		execute_ssh_command(cmd)
   
	system_type = None
	output = subprocess.check_output(["cat", "/etc/os-release"]).decode().strip()
	if re.search(r"debian", output, re.IGNORECASE):
		system_type = "debian"
	elif re.search(r"Red Hat", output, re.IGNORECASE):
		system_type = "redhat"
	elif re.search(r"openSSUE", output, re.IGNORECASE):
		system_type = "openSSUE"
	elif re.search(r"Arch", output, re.IGNORECASE):
		system_type = "Arch"
  
	sub_meniu = tk.Tk()
	sub_meniu.title("Actiune pe servicii/procese")
	sub_meniu.geometry("500x500")

	image = Image.open("/home/student/project-2023/stitch-work.jpg")
	image = image.resize((500, 500), Image.ANTIALIAS)
	background_image = ImageTk.PhotoImage(image)

	background_label = tk.Label(sub_meniu, image=background_image)
	background_label.place(x=0, y=0, relwidth=1, relheight=1)

	style = ttk.Style(sub_meniu)
	style.configure("TFrame", background="#b3c6e7")
	style.configure("TButton", background="#441f8a", foreground="#ffffff", font=("Arial", 12, "bold"))
	style.configure("TLabel", background="#b3c8e7", foreground="#000000", font=("Arial", 12))
	style.configure("TCombobox", background="#324ba9", foreground="#ffffff", font=("Arial", 12))
	style.configure("TEntry", background="#324ba9", foreground="#ffffff", font=("Arial", 12))

	frame = ttk.Frame(sub_meniu, style = "TFrame")
	frame.pack(padx=20, pady=20)
    
	label = ttk.Label(frame, text="Select an option:", style="TLabel")
	label.grid(row=0, column=0, padx=10, pady=10)
    
	input_box = ttk.Entry(frame, font=("Arial", 12), style="TEntry")
	input_box.grid(row=0, column=1, padx=10, pady=10)
    
	select_button = ttk.Button(frame, text="Select", command=select_option, style="TButton")
	select_button.grid(row=1, column=0,  padx=30, pady=30)

	back_button = ttk.Button(frame, text="Back", command=go_back, style="TButton")
	back_button.grid(row=1, column=1,  padx=30, pady=30)
    
	sub_meniu.mainloop()

def menu(conn, addr):
	def select_option():
		chosen_option = options_box.get()
		meniu.destroy()
		if chosen_option == "Oprire/pornire servicii/procese":
			opt1(conn, addr)
		elif chosen_option == "Copiere fisiere":
			opt2(conn, addr)
		elif chosen_option == "Instalare aplicatii/servicii":
			opt3(conn, addr)

	options = ["Oprire/pornire servicii/procese", "Copiere fisiere", "Instalare aplicatii/servicii"]
	
	meniu = tk.Tk()
	meniu.title("Menu")
	meniu.geometry("500x500")

	image = Image.open("/home/student/project-2023/stitch-ftw.jpg")
	image = image.resize((500, 500), Image.ANTIALIAS)
	background_image = ImageTk.PhotoImage(image)

	background_label = tk.Label(meniu, image=background_image)
	background_label.place(x=0, y=0, relwidth=1, relheight=1)

	style = ttk.Style()
	style.configure("TFrame", background="#b3c6e7")
	style.configure("TButton", background="#441f8a", foreground="#ffffff", font=("Arial", 12, "bold"))
	style.configure("TLabel", background="#b3c8e7", foreground="#000000", font=("Arial", 12))
	style.configure("TCombobox", background="#324ba9", foreground="#ffffff", font=("Arial", 12))
	frame = ttk.Frame(meniu, style = "TFrame")
	frame.pack(padx=20, pady=20)
    
	label = ttk.Label(frame, text="Select an option:", style="TLabel")
	label.grid(row=0, column=0, padx=10, pady=10)
    
	options_box = ttk.Combobox(frame, values=options, font=("Arial", 12), state="readonly", style = "TCombobox")
	options_box.grid(row=0, column=1, padx=10, pady=10)
	options_box.current(0)
    
	select_button = ttk.Button(frame, text="Select", command=select_option, style="TButton")
	select_button.grid(row=1, column=0, columnspan=2, padx=30, pady=30)
    
	meniu.mainloop()

def handle_client(conn, addr):

	print(f"[NEW CONNECTION] {addr} connected.")

	data = conn.recv(SIZE).decode(FORMAT)

	username, client_ip = data.split(",")
	
	global IP_CL
	IP_CL = client_ip

	global USER_CL
	USER_CL = username

	create_client_folder(username)
	folder_name = f"clients/{username}"
	os.chdir(folder_name)
	reset_files()
	
	with open("info-shh.txt", "w") as file:

		file.write(f"{username} {client_ip}")
	
	user = subprocess.check_output("whoami").decode().strip()
	send_public_key(conn, user)
	
	while True:
		#reset_files()
		options = [
			("Reseteaza fisier pentru capacitatea memoriei","storage-unit.txt", "free -h"),
			("Reseteaza fisier despre dispozitive hardware","hw-info.txt", "hwinfo --short"),
			("Reseteaza fisier despre dispozitive I/O","io.txt", "iostat"),
			("Reseteaza fisier despre procese active","processes.txt", "systemctl list-units --type=service --state=running"),
			("Reseteaza fisier despre temperatura","temp.txt", "sensors"),
			("Resetare fisier despre utilizatori si timpi de autentificare","login.txt", "lastlog"),
			("Reseteaza fisier pentru informatii de sistem","system.txt", "neofetch --stdout")
		]

		for option in options:
			menu_title, file_name, cmd = option
			output = execute_ssh_command(cmd)
			if output is not None:
				#print("[CLIENT] Command output:\n{output}")
				with open(file_name, "w") as file:
					file.write(f"Data: {datetime.datetime.now()}\n")
					file.write(f"{username}'s info:\n")
					file.write(output.strip())
					file.write(f"\n")

		time.sleep(300)

	os.chdir("..")
 
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

		menu_thread = threading.Thread(target=menu, args=(conn, addr))
		menu_thread.start()

		print(f"[ACTIVE CONNECTIONS] {threading.active_count() -1}")

if __name__ == "__main__":

	main()
#menu()

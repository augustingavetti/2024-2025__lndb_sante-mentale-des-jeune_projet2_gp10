import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

def receive_message():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            chat_area.config(state=tk.NORMAL)
            chat_area.insert(tk.END, "Serveur: " + message + "\n")
            chat_area.config(state=tk.DISABLED)
        except:
            break

def send_message():
    message = message_entry.get()
    message_entry.delete(0, tk.END)
    client_socket.send(message.encode('utf-8'))
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, "Vous: " + message + "\n")
    chat_area.config(state=tk.DISABLED)

def connect_to_server():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    discovery_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    discovery_socket.settimeout(5)
    discovery_socket.sendto(b"DISCOVER_SERVER", ('<broadcast>', 12345))
    
    try:
        while True:
            data, addr = discovery_socket.recvfrom(1024)
            if data == b"SERVER_IP":
                server_ip = addr[0]
                client_socket.connect((server_ip, 12345))
                chat_area.insert(tk.END, f"Connecté au serveur à {server_ip}\n")
                thread = threading.Thread(target=receive_message)
                thread.start()
                break
    except socket.timeout:
        chat_area.insert(tk.END, "Impossible de trouver le serveur.\n")

root = tk.Tk()
root.title("Chat Client")

chat_area = scrolledtext.ScrolledText(root, state=tk.DISABLED)
chat_area.pack(padx=10, pady=10)

message_entry = tk.Entry(root, width=50)
message_entry.pack(padx=10, pady=10)
message_entry.bind("<Return>", lambda event: send_message())

send_button = tk.Button(root, text="Envoyer", command=send_message)
send_button.pack(padx=10, pady=10)

thread = threading.Thread(target=connect_to_server)
thread.start()

root.mainloop()

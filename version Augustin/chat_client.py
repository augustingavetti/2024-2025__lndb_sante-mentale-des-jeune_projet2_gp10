import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
import time  # Ajout de l'importation du module time

def handle_client():
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        chat_area.config(state=tk.NORMAL)
        chat_area.insert(tk.END, "Client: " + message + "\n")
        chat_area.config(state=tk.DISABLED)

def send_message():
    message = message_entry.get()
    message_entry.delete(0, tk.END)
    client_socket.send(message.encode('utf-8'))
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, "Vous: " + message + "\n")
    chat_area.config(state=tk.DISABLED)

def start_server():
    global client_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(1)
    chat_area.insert(tk.END, "En attente de connexion...\n")
    
    client_socket, addr = server_socket.accept()
    chat_area.insert(tk.END, f"Connexion de {addr}\n")

    thread = threading.Thread(target=handle_client)
    thread.start()

def broadcast_ip():
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    while True:
        broadcast_socket.sendto(b"SERVER_IP", ('<broadcast>', 12345))
        time.sleep(5)

root = tk.Tk()
root.title("Chat Serveur")

chat_area = scrolledtext.ScrolledText(root, state=tk.DISABLED)
chat_area.pack(padx=10, pady=10)

message_entry = tk.Entry(root, width=50)
message_entry.pack(padx=10, pady=10)
message_entry.bind("<Return>", lambda event: send_message())

send_button = tk.Button(root, text="Envoyer", command=send_message)
send_button.pack(padx=10, pady=10)

thread = threading.Thread(target=start_server)


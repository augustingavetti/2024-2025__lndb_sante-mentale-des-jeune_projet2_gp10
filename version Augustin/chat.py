import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog

def receive_message():
    while True:
        try:
            message = conn.recv(1024).decode('utf-8')
            chat_area.config(state=tk.NORMAL)
            chat_area.insert(tk.END, f"{role}: " + message + "\n")
            chat_area.config(state=tk.DISABLED)
        except:
            break

def send_message():
    message = message_entry.get()
    message_entry.delete(0, tk.END)
    conn.send(message.encode('utf-8'))
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, "Vous: " + message + "\n")
    chat_area.config(state=tk.DISABLED)

def start_server():
    global conn
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(1)
    chat_area.insert(tk.END, "En attente de connexion...\n")
    conn, addr = server_socket.accept()
    chat_area.insert(tk.END, f"Connexion de {addr}\n")
    thread = threading.Thread(target=receive_message)
    thread.start()

def connect_to_server():
    global conn
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = simpledialog.askstring("Adresse IP", "Entrez l'adresse IP du serveur:")
    conn.connect((server_ip, 12345))
    thread = threading.Thread(target=receive_message)
    thread.start()

root = tk.Tk()
root.title("Chat Application")

chat_area = scrolledtext.ScrolledText(root, state=tk.DISABLED)
chat_area.pack(padx=10, pady=10)

message_entry = tk.Entry(root, width=50)
message_entry.pack(padx=10, pady=10)
message_entry.bind("<Return>", lambda event: send_message())

send_button = tk.Button(root, text="Envoyer", command=send_message)
send_button.pack(padx=10, pady=10)

role = simpledialog.askstring("Rôle", "Tapez 'serveur' pour démarrer le serveur, ou 'client' pour vous connecter:")
if role.lower() == "serveur":
    start_server()
elif role.lower() == "client":
    connect_to_server()
else:
    chat_area.insert(tk.END, "Rôle non valide.\n")

root.mainloop()


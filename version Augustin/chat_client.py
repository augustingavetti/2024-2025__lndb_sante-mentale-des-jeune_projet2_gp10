import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

def receive_message():
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        chat_area.config(state=tk.NORMAL)
        chat_area.insert(tk.END, "Serveur: " + message + "\n")
        chat_area.config(state=tk.DISABLED)

def send_message():
    message = message_entry.get()
    message_entry.delete(0, tk.END)
    client_socket.send(message.encode('utf-8'))
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, "Vous: " + message + "\n")
    chat_area.config(state=tk.DISABLED)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('adresse_ip_du_serveur', 12345))

root = tk.Tk()
root.title("Chat Client")

chat_area = scrolledtext.ScrolledText(root, state=tk.DISABLED)
chat_area.pack(padx=10, pady=10)

message_entry = tk.Entry(root, width=50)
message_entry.pack(padx=10, pady=10)
message_entry.bind("<Return>", lambda event: send_message())

send_button = tk.Button(root, text="Envoyer", command=send_message)
send_button.pack(padx=10, pady=10)

thread = threading.Thread(target=receive_message)
thread.start()

root.mainloop()

import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

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

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 12345))
server_socket.listen(1)

root = tk.Tk()
root.title("Chat Serveur")

chat_area = scrolledtext.ScrolledText(root, state=tk.DISABLED)
chat_area.pack(padx=10, pady=10)

message_entry = tk.Entry(root, width=50)
message_entry.pack(padx=10, pady=10)
message_entry.bind("<Return>", lambda event: send_message())

send_button = tk.Button(root, text="Envoyer", command=send_message)
send_button.pack(padx=10, pady=10)

print("En attente de connexion...")
client_socket, addr = server_socket.accept()
print(f"Connexion de {addr}")

thread = threading.Thread(target=handle_client)
thread.start()

root.mainloop()


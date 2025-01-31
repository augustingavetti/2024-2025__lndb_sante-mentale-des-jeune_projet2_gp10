import tkinter as tk
from tkinter import scrolledtext
import socket
import threading

def receive_message():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            chat_area.config(state=tk.NORMAL)
            chat_area.insert(tk.END, message + '\n')
            chat_area.config(state=tk.DISABLED)
        except:
            break

def send_message():
    message = message_entry.get()
    message_entry.delete(0, tk.END)
    client_socket.send(message.encode('utf-8'))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 5555))

root = tk.Tk()
root.title("Chat")

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

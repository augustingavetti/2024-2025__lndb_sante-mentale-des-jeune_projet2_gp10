import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog

class ChatClientGUI:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.nickname = simpledialog.askstring("Nickname", "Enter your nickname:")
        self.root = tk.Tk()
        self.root.title("Chat")

        self.chat_area = scrolledtext.ScrolledText(self.root, state='disabled', wrap='word')
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.message_entry = tk.Entry(self.root)
        self.message_entry.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)
        self.message_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def start_client(self):
        try:
            self.client.connect((self.host, self.port))
            threading.Thread(target=self.receive_messages, daemon=True).start()
            self.client.send(self.nickname.encode('utf-8'))
            self.root.mainloop()
        except ConnectionRefusedError:
            print("Unable to connect to the server.")

    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                self.chat_area.configure(state='normal')
                self.chat_area.insert(tk.END, message + "\n")
                self.chat_area.configure(state='disabled')
                self.chat_area.yview(tk.END)
            except:
                break

    def send_message(self, event=None):
        message = self.message_entry.get()
        if message.strip():
            self.client.send(f"{self.nickname}: {message}".encode('utf-8'))
            self.message_entry.delete(0, tk.END)

    def on_close(self):
        self.client.close()
        self.root.destroy()

class ChatServer:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.nicknames = []

    def start_server(self):
        self.server.bind((self.host, self.port))
        self.server.listen()
        print(f"Server running on {self.host}:{self.port}")

        while True:
            client, _ = self.server.accept()
            threading.Thread(target=self.handle_client, args=(client,)).start()

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def handle_client(self, client):
        client.send("NICKNAME".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        self.nicknames.append(nickname)
        self.clients.append(client)

        self.broadcast(f"{nickname} joined the chat!".encode('utf-8'))
        print(f"{nickname} joined the chat!")

        while True:
            try:
                message = client.recv(1024)
                self.broadcast(message)
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                nickname = self.nicknames.pop(index)
                self.broadcast(f"{nickname} left the chat.".encode('utf-8'))
                print(f"{nickname} left the chat.")
                client.close()
                break

if __name__ == "__main__":
    mode = simpledialog.askstring("Mode", "Enter 'server' to start a server or 'client' to join a chat:")

    if mode == 'server':
        server = ChatServer()
        server.start_server()
    elif mode == 'client':
        client = ChatClientGUI()
        client.start_client()
    else:
        print("Invalid mode. Please restart and enter 'server' or 'client'.")
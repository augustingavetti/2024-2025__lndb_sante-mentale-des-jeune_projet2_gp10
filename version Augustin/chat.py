import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Fonction pour gérer les messages reçus
def recevoir_messages(client_socket, chat_box):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            chat_box.config(state=tk.NORMAL)
            chat_box.insert(tk.END, message + '\n')
            chat_box.config(state=tk.DISABLED)
        except:
            chat_box.config(state=tk.NORMAL)
            chat_box.insert(tk.END, "Connexion perdue.\n")
            chat_box.config(state=tk.DISABLED)
            client_socket.close()
            break

# Fonction pour envoyer un message
def envoyer_message(client, entry, chat_box, root):
    message = entry.get()
    if message.strip():  # Vérifie que le message n'est pas vide
        try:
            if message.lower() == "exit":
                client.send("Déconnexion".encode('utf-8'))
                client.close()
                root.destroy()
            else:
                client.send(message.encode('utf-8'))
                chat_box.config(state=tk.NORMAL)
                chat_box.insert(tk.END, "Vous: " + message + '\n')
                chat_box.config(state=tk.DISABLED)
            entry.delete(0, tk.END)
        except:
            messagebox.showerror("Erreur", "Impossible d'envoyer le message. Vérifiez votre connexion.")

# Fonction principale du client
def demarrer_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    root = tk.Tk()
    root.title("Chat Client")
    
    tk.Label(root, text="Adresse IP du serveur:").pack()
    ip_entry = tk.Entry(root)
    ip_entry.pack()
    ip_entry.insert(0, "127.0.0.1")
    
    chat_box = scrolledtext.ScrolledText(root, state=tk.DISABLED, wrap=tk.WORD, width=50, height=20)
    chat_box.pack(pady=10)
    
    entry = tk.Entry(root, width=40)
    entry.pack(side=tk.LEFT, padx=10)
    send_button = tk.Button(root, text="Envoyer", command=lambda: envoyer_message(client, entry, chat_box, root))
    send_button.pack(side=tk.RIGHT, padx=10)
    
    def connecter():
        hote = ip_entry.get()
        port = 12345
        try:
            client.connect((hote, port))
            chat_box.config(state=tk.NORMAL)
            chat_box.insert(tk.END, "Connecté au serveur\n")
            chat_box.config(state=tk.DISABLED)
            threading.Thread(target=recevoir_messages, args=(client, chat_box), daemon=True).start()
        except:
            messagebox.showerror("Erreur", "Impossible de se connecter au serveur. Vérifiez l'adresse IP et le port.")
            client.close()
    
    connect_button = tk.Button(root, text="Se connecter", command=connecter)
    connect_button.pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    demarrer_client()

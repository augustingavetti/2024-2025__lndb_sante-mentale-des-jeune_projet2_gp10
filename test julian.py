# gui.py
import tkinter as tk
from tkinter import messagebox
from app import MentalHealthApp  

class MentalHealthGUI:
    def __init__(self, root):
        self.app = MentalHealthApp()  # Instance de la logique de l'application
        self.root = root
        self.root.title("Suivi de la Santé Mentale")
        self.root.geometry("600x400")
        self.root.config(bg="#003366")  # Couleur de fond bleu foncé
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Connexion", font=("Helvetica", 24, "bold"), bg="#003366", fg="white").pack(pady=20)

        tk.Label(self.root, text="Nom d'utilisateur:", font=("Helvetica", 14), bg="#003366", fg="white").pack(pady=5)
        self.username_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Mot de passe:", font=("Helvetica", 14), bg="#003366", fg="white").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*", font=("Helvetica", 14))
        self.password_entry.pack(pady=5)

        button_style = {
            'font': ("Helvetica", 14),
            'bg': "#00509e",
            'fg': "white",
            'width': 15,
            'height': 1,
            'activebackground': "#003366"
        }

        tk.Button(self.root, text="Se connecter", command=self.login, **button_style).pack(pady=20)
        tk.Button(self.root, text="Créer un compte", command=self.create_account_screen, **button_style).pack(pady=5)

    def create_account_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Créer un Compte", font=("Helvetica", 24, "bold"), bg="#003366", fg="white").pack(pady=20)

        tk.Label(self.root, text="Nom d'utilisateur:", font=("Helvetica", 14), bg="#003366", fg="white").pack(pady=5)
        self.new_username_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.new_username_entry.pack(pady=5)

        tk.Label(self.root, text="Mot de passe:", font=("Helvetica", 14), bg="#003366", fg="white").pack(pady=5)
        self.new_password_entry = tk.Entry(self.root, show="*", font=("Helvetica", 14))  # Correction ici
        self.new_password_entry.pack(pady=5)

        button_style = {
            'font': ("Helvetica", 14),
            'bg': "#00509e",
            'fg': "white",
            'width': 15,
            'height': 1,
            'activebackground': "#003366"
        }

        tk.Button(self.root, text="Créer", command=self.create_account, **button_style).pack(pady=20)
        tk.Button(self.root, text="Retour à la connexion", command=self.create_login_screen, **button_style).pack(pady=5)

    def create_account(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()

        if self.app.create_account(username, password):
            messagebox.showinfo("Succès", "Compte créé avec succès!")
            self.create_login_screen()
        else:
            messagebox.showwarning("Avertissement", "Ce nom d'utilisateur est déjà pris.")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.app.login(username, password):
            messagebox.showinfo("Succès", "Connexion réussie!")
            self.create_home_screen()
        else:
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")

    def create_home_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Bienvenue!", font=("Helvetica", 24, "bold"), bg="#003366", fg="white").pack(pady=20)

        button_style = {
            'font': ("Helvetica", 14),
            'bg': "#00509e",
            'fg': "white",
            'width': 25,
            'height': 1,
            'activebackground': "#003366"
        }
        tk.Label(self.root, text="Le QCM va maintenant commmencer", font=("Colibri", 20, "bold"), bg="#003366", fg="white").pack(pady=20)
        tk.Button(self.root, text="Continuer", command=self.first_question, **button_style).pack(pady=20,)
        
        
        
    
        


        # Ajoutez ici d'autres éléments de l'interface utilisateur pour l'écran d'accueil



    # def clear_screen(self):
    #     for widget in self.root.winfo_children():
    #         widget.destroy()  # Détruire tous les widgets de l'écran actuel
            

    def first_question(self):
        for widget in self.root.winfo_children():
            widget.destroy()       
        tk.Label(self.root, text="Comment vous-sentez vous ?", font=("Helvetica", 14), bg="#003366", fg="white").pack(pady=5) 
        tk.Button(self.root, text="Très bien", command=self.second_question,).pack(pady=20,)
        tk.Button(self.root, text="bien", command=self.second_question,).pack(pady=20,)
        tk.Button(self.root, text="moyen", command=self.second_question,).pack(pady=20,)
        tk.Button(self.root, text="Pas ouf", command=self.second_question,).pack(pady=20,)
        tk.Button(self.root, text="Pas bien", command=self.second_question,).pack(pady=20,)
 
    def second_question(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, text="Quelle a été votre charge de travail cette semaine ?", font=("Helvetica", 14), bg="#003366", fg="white").pack(pady=5) 
        tk.Button(self.root, text="Très bien", command=self.third_question,).pack(pady=20,)
        tk.Button(self.root, text="bien", command=self.third_question,).pack(pady=20,)
        tk.Button(self.root, text="un peu trop", command=self.third_question,).pack(pady=20,)
        tk.Button(self.root, text="importante", command=self.third_question,).pack(pady=20,)
        tk.Button(self.root, text="Beaucoup trop", command=self.third_question,).pack(pady=20,)

    def third_question(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, text="Avez vous bien mangé cette semaine ?", font=("Helvetica", 14), bg="#003366", fg="white").pack(pady=5) 
        tk.Button(self.root, text="Très bien", command=self.fourth_question,).pack(pady=20,)
        tk.Button(self.root, text="bien", command=self.fourth_question,).pack(pady=20,)
        tk.Button(self.root, text="juste à ma faim", command=self.fourth_question,).pack(pady=20,)
        tk.Button(self.root, text="peu", command=self.fourth_question,).pack(pady=20,)
        tk.Button(self.root, text="presque pas", command=self.fourth_question,).pack(pady=20,)    

    def fourth_question(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, text="Quelle a été la relation avec ta famille ?", font=("Helvetica", 14), bg="#003366", fg="white").pack(pady=5) 
        tk.Button(self.root, text="Parfaite", command=self.five_question,).pack(pady=20,)
        tk.Button(self.root, text="Bien", command=self.five_question,).pack(pady=20,)
        tk.Button(self.root, text="ça va", command=self.five_question,).pack(pady=20,)
        tk.Button(self.root, text="J'ai vu mieux", command=self.five_question,).pack(pady=20,)
        tk.Button(self.root, text="Pas bien du tout", command=self.five_question,).pack(pady=20,)     

    def five_question(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, text="Autre question ?", font=("Helvetica", 14), bg="#003366", fg="white").pack(pady=5)
            



# Lancer l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = MentalHealthGUI(root)
    root.mainloop()
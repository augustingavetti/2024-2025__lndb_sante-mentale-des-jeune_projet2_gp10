import tkinter as tk
from tkinter import messagebox, scrolledtext
from app import MentalHealthApp
from simple_graphs import create_bar_graph
from data import questions, encouragements
from dictionary import questions_and_answers
import random

class MentalHealthGUI:
    def __init__(self, root):
        self.app = MentalHealthApp()
        self.root = root
        self.root.title("Application de Santé Mentale")
        self.root.geometry("800x600")
        self.root.configure(bg="#003366")
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Bienvenue", font=("Helvetica", 24), bg="#003366", fg="white").pack(pady=20)
        
        tk.Label(self.root, text="Nom d'utilisateur:", font=("Helvetica", 14), bg="#003366", fg="white").pack()
        self.username_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.username_entry.pack()
        
        tk.Label(self.root, text="Mot de passe:", font=("Helvetica", 14), bg="#003366", fg="white").pack()
        self.password_entry = tk.Entry(self.root, show="*", font=("Helvetica", 14))
        self.password_entry.pack()
        
        button_style = {"font": ("Helvetica", 14), "bg": "#00509e", "fg": "white"}
        tk.Button(self.root, text="Se connecter", command=self.login, **button_style).pack(pady=10)
        tk.Button(self.root, text="Créer un compte", command=self.create_account_screen, **button_style).pack(pady=5)

    def create_account_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Créer un compte", font=("Helvetica", 24), bg="#003366", fg="white").pack(pady=20)
        
        tk.Label(self.root, text="Nouveau nom d'utilisateur:", font=("Helvetica", 14), bg="#003366", fg="white").pack()
        self.new_username_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.new_username_entry.pack()
        
        tk.Label(self.root, text="Nouveau mot de passe:", font=("Helvetica", 14), bg="#003366", fg="white").pack()
        self.new_password_entry = tk.Entry(self.root, show="*", font=("Helvetica", 14))
        self.new_password_entry.pack()
        
        button_style = {"font": ("Helvetica", 14), "bg": "#00509e", "fg": "white"}
        tk.Button(self.root, text="Créer", command=self.create_account, **button_style).pack(pady=10)
        tk.Button(self.root, text="Retour", command=self.create_login_screen, **button_style).pack(pady=5)

    def create_home_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Accueil", font=("Helvetica", 24), bg="#003366", fg="white").pack(pady=20)
        
        button_style = {"font": ("Helvetica", 14), "bg": "#00509e", "fg": "white"}
        tk.Button(self.root, text="Commencer le questionnaire", command=self.start_questionnaire, **button_style).pack(pady=10)
        tk.Button(self.root, text="Voir le dernier bilan", command=self.show_latest_summary, **button_style).pack(pady=10)
        tk.Button(self.root, text="Voir le bilan global", command=self.show_overall_summary, **button_style).pack(pady=10)

    def start_questionnaire(self):
        self.clear_screen()
        self.current_question = 0
        self.responses = {}
        self.show_question()

    def show_question(self):
        if self.current_question < len(questions_and_answers):
            question_data = questions_and_answers[self.current_question]
            tk.Label(self.root, text=question_data["question"], font=("Helvetica", 16), bg="#003366", fg="white").pack(pady=20)
    
            for answer in question_data["answers"]:
                tk.Button(self.root, text=answer["text"], 
                          command=lambda a=answer: self.answer_question(a),
                          font=("Helvetica", 12), bg="#00509e", fg="white").pack(pady=5)
        else:
            self.show_daily_summary()

    def answer_question(self, answer):
        self.responses[questions_and_answers[self.current_question]["question"]] = answer
        self.current_question += 1
        self.clear_screen()
        
        if self.current_question < len(questions_and_answers):
            tk.Label(self.root, text=f"Réponse enregistrée : {answer['text']}", font=("Helvetica", 14), bg="#003366", fg="white").pack(pady=20)
            tk.Button(self.root, text="Continuer", command=self.show_question,
                      font=("Helvetica", 14), bg="#00509e", fg="white").pack(pady=20)
        else:
            self.show_daily_summary()

    def show_daily_summary(self):
        self.clear_screen()
        tk.Label(self.root, text="Résumé du jour", font=("Helvetica", 24, "bold"), bg="#003366", fg="white").pack(pady=20)
    
        emotions_count = {"Positif": 0, "Neutre": 0, "Négatif": 0}
        for response in self.responses.values():
            emotions_count[response["category"]] += 1
    
        create_bar_graph(self.root, emotions_count, "Résumé des réponses du jour")
    
        encouragement = random.choice(encouragements)
        tk.Label(self.root, text=encouragement, font=("Helvetica", 14), bg="#003366", fg="white", wraplength=600).pack(pady=20)
    
        tk.Button(self.root, text="Retour à l'accueil", command=self.create_home_screen,
                  font=("Helvetica", 14), bg="#00509e", fg="white").pack(pady=20)

    def show_latest_summary(self):
        summary = self.app.get_latest_summary()
        if summary:
            self.show_summary(summary, "Dernier bilan hebdomadaire")
        else:
            messagebox.showinfo("Information", "Pas encore de bilan hebdomadaire disponible.")

    def show_overall_summary(self):
        summary = self.app.get_overall_summary()
        if summary:
            self.show_summary(summary, "Bilan global")
        else:
            messagebox.showinfo("Information", "Pas encore assez de données pour un bilan global.")

    def show_summary(self, summary, title):
        self.clear_screen()
        tk.Label(self.root, text=title, font=("Helvetica", 24, "bold"), bg="#003366", fg="white").pack(pady=20)

        create_bar_graph(self.root, summary, "Résumé des émotions")

        encouragement = random.choice(encouragements)
        tk.Label(self.root, text=encouragement, font=("Helvetica", 14), bg="#003366", fg="white", wraplength=600).pack(pady=20)

        tk.Button(self.root, text="Retour à l'accueil", command=self.create_home_screen,
                  font=("Helvetica", 14), bg="#00509e", fg="white").pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.app.login(username, password):
            self.create_home_screen()
        else:
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")

    def create_account(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()
        if self.app.create_account(username, password):
            messagebox.showinfo("Succès", "Compte créé avec succès!")
            self.create_login_screen()
        else:
            messagebox.showerror("Erreur", "Ce nom d'utilisateur est déjà pris.")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MentalHealthGUI(root)
    root.mainloop()
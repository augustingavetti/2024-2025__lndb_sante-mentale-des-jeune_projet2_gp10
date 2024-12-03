import tkinter as tk
from tkinter import messagebox, scrolledtext
from app import MentalHealthApp
from dictionary import emotion_dict
from simple_graphs import create_bar_graph

class MentalHealthGUI:
    def __init__(self, root):
        self.app = MentalHealthApp()
        self.root = root
        self.root.title("Suivi de la Santé Mentale")
        self.root.geometry("800x600")
        self.root.config(bg="#003366")
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

        button_style = {'font': ("Helvetica", 14), 'bg': "#00509e", 'fg': "white", 'width': 15, 'height': 1}
        tk.Button(self.root, text="Se connecter", command=self.login, **button_style).pack(pady=20)
        tk.Button(self.root, text="Créer un compte", command=self.create_account_screen, **button_style).pack(pady=5)

    def create_account_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Créer un compte", font=("Helvetica", 24, "bold"), bg="#003366", fg="white").pack(pady=20)

        tk.Label(self.root, text="Nom d'utilisateur:", font=("Helvetica", 14), bg="#003366", fg="white").pack(pady=5)
        self.new_username_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.new_username_entry.pack(pady=5)

        tk.Label(self.root, text="Mot de passe:", font=("Helvetica", 14), bg="#003366", fg="white").pack(pady=5)
        self.new_password_entry = tk.Entry(self.root, show="*", font=("Helvetica", 14))
        self.new_password_entry.pack(pady=5)

        button_style = {'font': ("Helvetica", 14), 'bg': "#00509e", 'fg': "white", 'width': 15, 'height': 1}
        tk.Button(self.root, text="Créer", command=self.create_account, **button_style).pack(pady=20)
        tk.Button(self.root, text="Retour", command=self.create_login_screen, **button_style).pack(pady=5)

    def create_home_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Bienvenue!", font=("Helvetica", 24, "bold"), bg="#003366", fg="white").pack(pady=20)

        button_style = {'font': ("Helvetica", 14), 'bg': "#00509e", 'fg': "white", 'width': 25, 'height': 1}
        tk.Button(self.root, text="Commencer le questionnaire", command=self.start_questionnaire, **button_style).pack(pady=10)
        tk.Button(self.root, text="Voir le dernier bilan", command=self.show_latest_summary, **button_style).pack(pady=10)
        tk.Button(self.root, text="Voir le bilan global", command=self.show_overall_summary, **button_style).pack(pady=10)

    def start_questionnaire(self):
        self.clear_screen()
        self.questions = self.app.start_questionnaire()
        self.current_question = 0
        self.responses = {}
        self.show_question()

    def show_question(self):
        if self.current_question < len(self.questions):
            question = self.questions[self.current_question]
            tk.Label(self.root, text=question, font=("Helvetica", 16), bg="#003366", fg="white").pack(pady=20)

            for emotion, description in emotion_dict.items():
                tk.Button(self.root, text=description, command=lambda e=emotion: self.answer_question(e),
                          font=("Helvetica", 12), bg="#00509e", fg="white").pack(pady=5)
        else:
            self.app.submit_response(self.responses)
            self.show_daily_summary()

    def answer_question(self, emotion):
        self.responses[self.questions[self.current_question]] = emotion
        self.current_question += 1
        self.clear_screen()
        self.show_question()

    def show_daily_summary(self):
        self.clear_screen()
        tk.Label(self.root, text="Résumé du jour", font=("Helvetica", 24, "bold"), bg="#003366", fg="white").pack(pady=20)

        emotions_count = {emotion: list(self.responses.values()).count(emotion) for emotion in emotion_dict.keys()}
        create_bar_graph(self.root, emotions_count, "Résumé des émotions du jour")

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
            self.show_summary({"data": summary}, "Bilan global sur 7 semaines")
        else:
            messagebox.showinfo("Information", "Pas encore assez de données pour un bilan global.")

    def show_summary(self, summary, title):
        self.clear_screen()
        tk.Label(self.root, text=title, font=("Helvetica", 24, "bold"), bg="#003366", fg="white").pack(pady=20)

        create_bar_graph(self.root, summary["data"], "Résumé des émotions")

        if "encouragement" in summary:
            text_widget = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=60, height=4, font=("Helvetica", 12))
            text_widget.insert(tk.END, summary["encouragement"])
            text_widget.config(state=tk.DISABLED)
            text_widget.pack(pady=20)

        tk.Button(self.root, text="Retour à l'accueil", command=self.create_home_screen,
                  font=("Helvetica", 14), bg="#00509e", fg="white").pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.app.login(username, password):
            messagebox.showinfo("Succès", "Connexion réussie!")
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
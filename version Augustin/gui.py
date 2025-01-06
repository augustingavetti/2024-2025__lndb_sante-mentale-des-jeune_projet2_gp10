import json
import os
import tkinter as tk
from tkinter import messagebox
from collections import defaultdict
import random
from dictionary import questions_and_answers
from app import MentalHealthApp
from simple_graphs import create_bar_graph
from data import questions, encouragements



class MentalHealthApp:
    logins_pwds_json = 'logins_pwds.json'
    responses_json = 'responses.json'

    def __init__(self):
        self.dico_users = self.read_json_file(self.logins_pwds_json)
        self.responses = self.read_json_file(self.responses_json)
        self.current_user = None

    def read_json_file(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return json.load(file)
        return {}

    def write_json_file(self, file_path, data):
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def create_account(self, login, pwd):
        if login not in self.dico_users:
            self.dico_users[login] = pwd
            self.write_json_file(self.logins_pwds_json, self.dico_users)
            self.responses[login] = []
            self.write_json_file(self.responses_json, self.responses)
            return True
        return False

    def login(self, login, pwd):
        if login in self.dico_users and self.dico_users[login] == pwd:
            self.current_user = login
            return True
        return False

    def save_response(self, response):
        if self.current_user:
            self.responses[self.current_user].append(response)
            self.write_json_file(self.responses_json, self.responses)

    # def generate_weekly_summary(self):
    #     if self.current_user:
    #         weekly_data = self.responses[self.current_user][-7:]
    #         summary = defaultdict(int)
    #         for response in weekly_data:
    #             for question, answer in response.items():
    #                 summary[answer] += 1
    #         encouragement = random.choice(["Continuez ainsi !", "Vous faites un excellent travail !"])
    #         return {"summary": summary, "encouragement": encouragement}
    #     return None

class MentalHealthGUI:
    def __init__(self, root):
        self.app = MentalHealthApp()
        self.root = root
        self.root.title("Application de Santé Mentale")
        self.root.geometry("800x700")
        self.root.configure(bg="#003366")
        self.create_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

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
        tk.Button(self.root, text="Répondre au questionnaire", command=self.start_questionnaire, **button_style).pack(pady=10)
        tk.Button(self.root, text="Voir le dernier résumé", command=self.view_summary, **button_style).pack(pady=5)
        tk.Button(self.root, text="résumé des 3 dernier graphiques",  **button_style).pack(pady=5)
        #  command=self.view_last_3_graph,
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.app.login(username, password):
            messagebox.showinfo("Succès", "Connexion réussie !")
            self.create_home_screen()
        else:
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")

    def create_account(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()
        if self.app.create_account(username, password):
            messagebox.showinfo("Succès", "Compte créé avec succès !")
            self.create_login_screen()
        else:
            messagebox.showerror("Erreur", "Le nom d'utilisateur existe déjà.")

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
        self.responses[questions_and_answers[self.current_question]["question"]] = answer["category"]
        self.current_question += 1
        self.clear_screen()

        if self.current_question < len(questions_and_answers):
            self.show_question()
        else:
            self.show_daily_summary()

    def show_daily_summary(self):
      self.clear_screen()
      tk.Label(self.root, text="Résumé du jour", font=("Helvetica", 24, "bold"), bg="#003366", fg="white").pack(pady=20)

    # Calcul des émotions
      emotions_count = {"Positif": 0, "Neutre": 0, "Négatif": 0}
      for category in self.responses.values():
          emotions_count[category] += 1

    # Créer le graphique
      create_bar_graph(self.root, emotions_count, title="Résumé des réponses d'aujourd'hui",
                       colors=["#4caf50", "#ffeb3b", "#f44336"])

    # Message d'encouragement
      encouragement = random.choice (encouragements)
      tk.Label(self.root, text=encouragement, font=("Helvetica", 14), bg="#003366", fg="white", wraplength=600).pack(pady=20)

      tk.Button(self.root, text="Retour à l'accueil", command=self.create_home_screen,
              font=("Helvetica", 14), bg="#00509e", fg="white").pack(pady=20)
    

    def view_summary(self):  
      self.clear_screen()
      if tk.Button(self.root, text="Retour à l'accueil", command=self.create_home_screen,
               font=("Helvetica", 14), bg="#00509e", fg="white").pack(pady=20):
         tk.Label(self.root, text="Résumé du jour", font=("Helvetica", 24, "bold"), bg="#003366", fg="white").pack(pady=20)
      emotions_count = {"Positif": 0, "Neutre": 0, "Négatif": 0}
      for category in self.responses.values():
            emotions_count[category] += 1
      create_bar_graph(self.root, emotions_count, title="Résumé des réponses d'aujourd'hui",
                         colors=["#4caf50", "#ffeb3b", "#f44336"])
      encouragement = random.choice (encouragements)
      tk.Label(self.root, text=encouragement, font=("Helvetica", 14), bg="#003366", fg="white", wraplength=600).pack(pady=20)
      tk.Button(self.root, text="Retour à l'accueil", command=self.create_home_screen,
               font=("Helvetica", 14), bg="#00509e", fg="white").pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    gui = MentalHealthGUI(root)
    root.mainloop()
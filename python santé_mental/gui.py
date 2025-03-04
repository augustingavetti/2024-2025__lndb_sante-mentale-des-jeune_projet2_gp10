import json
import os
import tkinter as tk
from tkinter import messagebox
from simple_graphs import create_bar_graph
from data import questions, encouragements
import csv
import webbrowser
from collections import defaultdict
import random
from dictionary import questions_and_answers
from tkinter import scrolledtext
import subprocess
import os

class MentalHealthApp:
    def export_responses_to_csv(self, filename="responses.csv"):
        if not self.responses:
            print("Aucune réponse à exporter.")
            return
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Utilisateur", "Question", "Réponse"])
            for user, user_responses in self.responses.items():
                for response in user_responses:
                    for question, answer in response.items():
                        writer.writerow([user, question, answer])
        print(f"Les réponses ont été exportées avec succès dans {filename}.")

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

    def calculate_weekly_summary(self):
        emotions_count = {"Positif": 0, "Neutre": 0, "Négatif": 0}
        total_responses = 0
        for user_responses in self.responses.values():
            for response in user_responses:
                for category in response.values():
                    emotions_count[category] += 1
                    total_responses += 1
        if total_responses > 0:
            for key in emotions_count:
                emotions_count[key] /= total_responses
        return emotions_count

class MentalHealthGUI:
    def __init__(self, root):
        self.app = MentalHealthApp()
        self.root = root
        self.root.title("Application de Santé Mentale")
        self.root.geometry("800x657")
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
        tk.Button(self.root, text="FAQ", command=self.open_faq, **button_style).pack(pady=5)
        tk.Button(self.root, text="Moyenne des résumés", command=self.moy_summary, **button_style).pack(pady=5)
        link = tk.Label(self.root, text="Pour plus d'informations sur la santé mentale, cliquez ici ", font=("Helvetica", 15), bg="#003366", fg="white", wraplength=400, cursor="hand2")
        link.pack(pady=50)
        link.bind("<Button-1>", lambda e: webbrowser.open_new("https://www.psycom.org/sorienter/les-lignes-decoute/"))
        link = tk.Label(self.root, text="Pour des livres sur la santé mentale, cliquez ici", font=("Helvetica", 15), bg="#003366", fg="white", wraplength=600, cursor="hand2")
        link.pack(pady=50)
        link.bind("<Button-1>", lambda e: webbrowser.open_new("https://www.babelio.com/livres-/Sante-mentale/78415"))
    
    def open_faq(self):
        base_path = os.path.dirname(__file__)
        faq_path = os.path.join(base_path, "FAQ.py")
        subprocess.Popen(["python", faq_path])

    def export_data_to_csv(self):
        # Récupérer les réponses de l'utilisateur actuel uniquement
        current_user_responses = self.app.responses.get(self.app.current_user, [])
        if not current_user_responses:
            messagebox.showerror("Erreur", "Aucune donnée à exporter.")
            return
        # Définir le nom du fichier CSV
        filename = f"{self.app.current_user}_responses.csv"
        # Écrire les données dans le fichier CSV
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Question", "Réponse"])
            for response in current_user_responses:
                for question, answer in response.items():
                    writer.writerow([question, answer])
        messagebox. howinfo("Succès", f"Les données ont été exportées dans le fichier {filename}.")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.app.login(username, password):
            self.app.current_user = username  # Définir l'utilisateur actuel
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
        emotions_count = {"Positif": 0, "Neutre": 0, "Négatif": 0}
        for category in self.responses.values():
            emotions_count[category] += 1
        create_bar_graph(self.root, emotions_count, title="Résumé des réponses d'aujourd'hui",
                         colors=["#4caf50", "#ffeb3b", "#f44336"])
        encouragement = random.choice(encouragements)
        tk.Label(self.root, text=encouragement, font=("Helvetica", 14), bg="#003366", fg="white", wraplength=600).pack(pady=20)
        tk.Button(self.root, text="Retour à l'accueil", command=self.create_home_screen,
                  font=("Helvetica", 14), bg="#00509e", fg="white").pack(pady=20)
        # Enregistrer les réponses pour l'utilisateur actuel
        self.app.save_response(self.responses)

    def view_summary(self):
        self.clear_screen()
        tk.Label(self.root, text="Résumé du jour", font=("Helvetica", 24, "bold"), bg="#003366", fg="white").pack(pady=20)
        tk.Button(self.root, text="Retour à l'accueil", command=self.create_home_screen,
                  font=("Helvetica", 14), bg="#00509e", fg="white").pack(pady=20)
        emotions_count = {"Positif": 0, "Neutre": 0, "Négatif": 0}
        for category in self.responses.values():
            emotions_count[category] += 1
        create_bar_graph(self.root, emotions_count, title="Résumé des réponses d'aujourd'hui",
                         colors=["#4caf50", "#ffeb3b", "#f44336"])
        if emotions_count["Négatif"] > 4:
            message = "Mbappé va bientôt venir te voir pour te remonter le morale !!!"
        else:
            encouragement = random.choice(encouragements)
            message = encouragement
        if emotions_count["Positif"] > 4:
            message = "Tu vas très bien, Mbappé te salut de loin."
        tk.Label(self.root, text=message, font=("Helvetica", 14), bg="#003366", fg="white", wraplength=600).pack(pady=20)
        tk.Button(self.root, text="Retour à l'accueil", command=self.create_home_screen, font=("Helvetica", 14), bg="#00509e", fg="white").pack(pady=20)

    def moy_summary(self):
        self.clear_screen()
        tk.Label(self.root, text="Résumé des derniers questionnaires", font=("Helvetica", 24, "bold"), bg="#003366", fg="white").pack(pady=20)
        # Récupérer les réponses de l'utilisateur actuel uniquement
        current_user_responses = self.app.responses.get(self.app.current_user, [])
        # Debug : Afficher les réponses de l'utilisateur actuel
        print("Réponses de l'utilisateur actuel :", current_user_responses)
        # Vérifier s'il y a des réponses
        if len(current_user_responses) == 0:
            tk.Label(self.root, text="Aucune donnée disponible.", font=("Helvetica", 14), bg="#003366", fg="white").pack(pady=20)
            tk.Button(self.root, text="Retour à l'accueil", command=self.create_home_screen,
                    font=("Helvetica", 14), bg="#00509e", fg="white").pack(pady=20)
            return
        # Prendre les 3 derniers questionnaires (si disponibles)
        last_three_responses = current_user_responses[-3:]
        # Compter les émotions
        emotions_count = {"Positif": 0, "Neutre": 0, "Négatif": 0}
        total_responses = 0
        for response in last_three_responses:
            print(f"Réponse analysée : {response}")  # Debug
            if isinstance(response, dict):
                for question, category in response.items():
                    print(f"Question : {question}, Catégorie : {category}")  # Debug
                    if category in emotions_count:
                        emotions_count[category] += 1
                        total_responses += 1
                    else:
                        print(f"Catégorie non reconnue : {category}")  # Debug
            else:
                print(f"Réponse inattendue : {response}")  # Debug
        # Vérifier si des réponses valides ont été trouvées
        if total_responses == 0:
            tk.Label(self.root, text="Pas assez de données pour générer un résumé.", font=("Helvetica", 14), bg="#003366", fg="white").pack(pady=20)
        else:
            # Calcul des moyennes
            for key in emotions_count:
                emotions_count[key] = round(emotions_count[key] / total_responses, 2)
            # Créer le graphique
            create_bar_graph(self.root, emotions_count, title="Moyenne des réponses des 3 derniers questionnaires",
                             colors=["#4caf50", "#ffeb3b", "#f44336"])
        # Bouton de retour
        tk.Button(self.root, text="Retour à l'accueil", command=self.create_home_screen,
                  font=("Helvetica", 14), bg="#00509e", fg="white").pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    gui = MentalHealthGUI(root)
    root.mainloop()
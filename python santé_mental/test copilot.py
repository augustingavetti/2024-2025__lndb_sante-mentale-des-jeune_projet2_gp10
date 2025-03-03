import json
import os
import tkinter as tk
from tkinter import messagebox
from simple_graphs import create_bar_graph
from data import questions, encouragements
import csv
import webbrowser
import random
from dictionary import questions_and_answers
from chat_client import rechercher_questions, faq_data


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
        tk.Button(self.root, text="Résumé de la semaine", command=self.view_weekly_summary, **button_style).pack(pady=5)
        tk.Button(self.root, text="FAQ", command=self.open_faq_window, **button_style).pack(pady=5)

        link = tk.Label(self.root, text="Pour plus d'informations sur la santé mentale, cliqué ici : https://baronmag.com/2018/02/ouvrages-sante-mentale/", font=("Helvetica", 15), bg="#003366", fg="white", wraplength=600, cursor="hand2")
        link.pack(pady=200)
        link.bind("<Button-1>", lambda e: webbrowser.open_new("https://baronmag.com/2018/02/ouvrages-sante-mentale/"))

    def open_faq_window(self):
        faq_window = tk.Toplevel(self.root)
        faq_window.title("FAQ Santé Mentale")
        faq_window.geometry("600x500")
        faq_window.configure(bg="#ADD8E6")

        # Label de titre
        title_label = tk.Label(faq_window, text="FAQ Santé Mentale", font=("Arial", 16, "bold"), bg="#ADD8E6")
        title_label.pack(pady=10)

        # Barre de recherche
        frame_search = tk.Frame(faq_window, bg="#ADD8E6")
        frame_search.pack(pady=5)

        entry_search = tk.Entry(frame_search, font=("Arial", 14), width=30)
        entry_search.pack(side="left", padx=5)

        btn_search = tk.Button(frame_search, text="Rechercher", font=("Arial", 12), command=lambda: self.afficher_resultats(entry_search, frame_results, selected_category))
        btn_search.pack(side="left")

        # Sélecteur de catégories
        categories = [(0, "Toutes")] + list(faq_data["categories"].items())
        selected_category = tk.IntVar(value=0)

        frame_categories = tk.Frame(faq_window, bg="#ADD8E6")
        frame_categories.pack(pady=10)

        for cat_id, cat_nom in categories:
            rb = tk.Radiobutton(frame_categories, text=cat_nom, variable=selected_category, value=cat_id, bg="#ADD8E6")
            rb.pack(anchor="w")

        # Frame pour les résultats
        frame_results = tk.Frame(faq_window, bg="#ADD8E6")
        frame_results.pack(pady=10)

    def afficher_resultats(self, entry_search, frame_results, selected_category):
        mot_cle = entry_search.get()
        categorie_id = selected_category.get()

        # Supprimer les anciens résultats
        for widget in frame_results.winfo_children():
            widget.destroy()

        # Recherche et affichage des résultats
        resultats = rechercher_questions(mot_cle, categorie_id if categorie_id != 0 else None)
        
        if resultats:
            for q, r in resultats:
                lbl_q = tk.Label(frame_results, text=q, font=("Arial", 12, "bold"), bg="#ADD8E6")
                lbl_r = tk.Label(frame_results, text=r, font=("Arial", 12), bg="#ADD8E6")
                lbl_q.pack(anchor="w", padx=10, pady=2)
                lbl_r.pack(anchor="w", padx=20, pady=2)
        else:
            lbl_no_result = tk.Label(frame_results, text="Aucun résultat trouvé.", font=("Arial", 12, "italic"), bg="#ADD8E6")
            lbl_no_result.pack(pady=10)

    # ... (le reste des méthodes de MentalHealthGUI)

if __name__ == "__main__":
    root = tk.Tk()
    gui = MentalHealthGUI(root)
    root.mainloop()
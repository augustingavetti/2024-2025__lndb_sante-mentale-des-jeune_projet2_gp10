# app.py
class MentalHealthApp:
    def __init__(self):
        self.users = {}  # Dictionnaire pour stocker les utilisateurs et mots de passe
        self.admin_code = "admin123"  # Code administrateur
        self.questions = [
            "Comment te sens-tu aujourd'hui ?",
            "Quelles émotions as-tu ressenties aujourd'hui ? (Choix multiples)",
            "Avez-vous rencontré des difficultés aujourd'hui ? (Oui/Non)",
            "Avez-vous eu des conflits avec des amis ou des proches ? (Oui/Non)"
        ]
        self.responses = []

    def create_account(self, username, password):
        if username in self.users:
            return False  # Nom d'utilisateur déjà pris
        else:
            self.users[username] = password
            return True  # Compte créé avec succès

    def login(self, username, password):
        return self.users.get(username) == password  # Vérifie les identifiants

    def start_questionnaire(self):
        self.responses = []  # Réinitialise les réponses
        return self.questions  # Retourne les questions

    def submit_response(self, response):
        self.responses.append(response)

    def get_summary(self):
        return self.responses  # Retourne les réponses pour le résumé

    def is_admin(self, code):
        return code == self.admin_code  # Vérifie si le code est correct
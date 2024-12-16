import json
import os

# Chemin vers le fichier JSON où les logins et mots de passe seront stockés
logins_pwds_json = 'logins_pwds.json'

def read_json_file(file_path):
    """Lit le fichier JSON et retourne un dictionnaire des logins et mots de passe."""
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {}

def write_json_file(file_path, data):
    """Écrit le dictionnaire des logins et mots de passe dans un fichier JSON."""
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def validate_user(login, pwd):
    """Valide l'utilisateur et ajoute son mot de passe s'il n'existe pas déjà."""
    if login not in dico_users:
        dico_users[login] = pwd
        write_json_file(logins_pwds_json, dico_users)
        print(f"Utilisateur {login} ajouté avec succès.")
    else:
        print(f"L'utilisateur {login} existe déjà.")

# Charger les logins et mots de passe existants depuis le fichier JSON
dico_users = read_json_file(logins_pwds_json)

# Exemple d'utilisation
if __name__ == "__main__":
    # Demander à l'utilisateur de saisir un login et un mot de passe
    login = input("Entrez votre login: ")
    pwd = input("Entrez votre mot de passe: ")
    validate_user(login, pwd)
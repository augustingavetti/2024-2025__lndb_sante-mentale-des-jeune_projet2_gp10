import tkinter as tk
from tkinter import ttk

# Dictionnaire contenant les questions et mots-clés
faq_data = {
    "categories": {
        1: "Anxiété",
        2: "Dépression",
        3: "Stress",
        4: "Bien-être",
        5: "Troubles du sommeil"
    },
    "questions": [
        {
            "question": "Comment gérer une crise d’anxiété ?",
            "reponse": "Essayez de respirer profondément, concentrez-vous sur un objet autour de vous et utilisez la technique 5-4-3-2-1 pour vous ancrer.",
            "categorie_id": 1,
            "mots_cles": ["anxiété", "crise", "respiration", "calme"]
        },
        {
            "question": "Quels sont les signes de la dépression ?",
            "reponse": "Les signes courants incluent une tristesse persistante, une perte d’intérêt pour les activités habituelles, une fatigue intense et des troubles du sommeil.",
            "categorie_id": 2,
            "mots_cles": ["dépression", "tristesse", "fatigue", "sommeil"]
        },
        {
            "question": "Comment réduire le stress au travail ?",
            "reponse": "Prenez des pauses régulières, organisez vos tâches par priorité et pratiquez la méditation ou la respiration profonde.",
            "categorie_id": 3,
            "mots_cles": ["stress", "travail", "méditation", "pause"]
        },
        {
            "question": "Quels sont les bienfaits du sport sur la santé mentale ?",
            "reponse": "Le sport libère des endorphines, réduit le stress et améliore la qualité du sommeil.",
            "categorie_id": 4,
            "mots_cles": ["sport", "endorphines", "sommeil", "stress"]
        },
        {
            "question": "Comment améliorer son sommeil naturellement ?",
            "reponse": "Évitez les écrans avant de dormir, créez une routine apaisante et limitez la caféine en soirée.",
            "categorie_id": 5,
            "mots_cles": ["sommeil", "caféine", "écrans", "routine"]
        }
    ]
}

def rechercher_questions(mot_cle="", categorie_id=None):
    """Recherche des questions en fonction d'un mot-clé ou d'une catégorie"""
    resultats = []
    for question in faq_data["questions"]:
        if mot_cle.lower() in [m.lower() for m in question["mots_cles"]] or mot_cle == "":
            if categorie_id is None or question["categorie_id"] == categorie_id:
                resultats.append((question["question"], question["reponse"]))
    return resultats

def afficher_resultats():
    """Affiche les résultats de la recherche dans l'interface"""
    mot_cle = entry_search.get()
    categorie_id = selected_category.get()

    # Supprimer les anciens résultats
    for widget in frame_results.winfo_children():
        widget.destroy()

    # Recherche et affichage des résultats
    resultats = rechercher_questions(mot_cle, categorie_id if categorie_id != 0 else None)
    
    if resultats:
        for q, r in resultats:
            lbl_q = tk.Label(frame_results, text=f"Q: {q}", font=("Arial", 12, "bold"), bg="#ADD8E6", wraplength=500, justify="left")
            lbl_r = tk.Label(frame_results, text=f"R: {r}", font=("Arial", 11), bg="#ADD8E6", wraplength=500, justify="left")
            lbl_q.pack(anchor="w", padx=10, pady=2)
            lbl_r.pack(anchor="w", padx=20, pady=2)
    else:
        lbl_no_result = tk.Label(frame_results, text="Aucun résultat trouvé.", font=("Arial", 12, "italic"), bg="#ADD8E6")
        lbl_no_result.pack(pady=10)

# Interface graphique
root = tk.Tk()
root.title("FAQ Santé Mentale")
root.geometry("600x500")
root.configure(bg="#ADD8E6")  # Fond bleu clair

# Label de titre
title_label = tk.Label(root, text="FAQ Santé Mentale", font=("Arial", 16, "bold"), bg="#ADD8E6")
title_label.pack(pady=10)

# Barre de recherche
frame_search = tk.Frame(root, bg="#ADD8E6")
frame_search.pack(pady=5)

entry_search = tk.Entry(frame_search, font=("Arial", 14), width=30)
entry_search.pack(side="left", padx=5)

btn_search = tk.Button(frame_search, text="Rechercher", font=("Arial", 12), command=afficher_resultats)
btn_search.pack(side="left")

# Sélecteur de catégories
categories = [(0, "Toutes")] + list(faq_data["categories"].items())
selected_category = tk.IntVar(value=0)

frame_categories = tk.Frame(root, bg="#ADD8E6")
frame_categories.pack(pady=10)

for cat_id, cat_nom in categories:
    btn_cat = ttk.Radiobutton(frame_categories, text=cat_nom, variable=selected_category, value=cat_id, command=afficher_resultats)
    btn_cat.pack(side="left", padx=5)

# Zone d'affichage des résultats
frame_results = tk.Frame(root, bg="#ADD8E6")
frame_results.pack(pady=10, fill="both", expand=True)

# Lancer l'application
root.mainloop()

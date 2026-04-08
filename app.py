from flask import Flask, render_template, request, redirect, url_for
# Import des fonctions Flask :
# Flask = créer l'application
# render_template = afficher du HTML
# request = récupérer les données du formulaire
# redirect + url_for = rediriger vers une page

import json
# Permet de lire/écrire dans un fichier JSON

import os
# Permet de vérifier si un fichier existe

app = Flask(__name__)
# Création de l'application Flask

FILE_NAME = "tasks.json"
# Nom du fichier où sont stockées les tâches


def load_tasks():
    # Fonction pour charger les tâches depuis le fichier JSON

    if not os.path.exists(FILE_NAME):
        return []
        # Si le fichier n'existe pas → retourne une liste vide

    with open(FILE_NAME, "r", encoding="utf-8") as file:
        return json.load(file)
        # Lit le fichier et retourne les données


def save_tasks(tasks):
    # Fonction pour sauvegarder les tâches dans le fichier JSON

    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)
        # Écrit les données dans le fichier avec une jolie mise en forme


@app.route("/")
def index():
    # Page principale

    tasks = load_tasks()
    # Récupère les tâches

    return render_template("index.html", tasks=tasks)
    # Envoie les tâches au HTML


@app.route("/add", methods=["POST"])
def add_task():
    # Route pour ajouter une tâche

    tasks = load_tasks()
    # Charge les tâches existantes

    new_task = {
        "id": len(tasks) + 1,
        # ID automatique (attention : peut poser problème si suppression)

        "title": request.form["title"],
        # Récupère le titre depuis le formulaire

        "description": request.form["description"],
        # Récupère la description

        "status": "Non faite",
        # Statut par défaut

        "due_date": request.form["due_date"]
        # Date choisie
    }

    tasks.append(new_task)
    # Ajoute la nouvelle tâche à la liste

    save_tasks(tasks)
    # Sauvegarde dans le fichier

    return redirect(url_for("index"))
    # Redirige vers la page principale


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    # Route pour supprimer une tâche

    tasks = load_tasks()

    tasks = [task for task in tasks if task["id"] != task_id]
    # Garde toutes les tâches sauf celle à supprimer

    save_tasks(tasks)

    return redirect(url_for("index"))


@app.route("/toggle/<int:task_id>")
def toggle_status(task_id):
    # Route pour changer le statut (faite / non faite)

    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            # Trouve la bonne tâche

            if task["status"] == "Non faite":
                task["status"] = "Faite"
            else:
                task["status"] = "Non faite"
            # Change le statut

            break

    save_tasks(tasks)

    return redirect(url_for("index"))


@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    # Route pour modifier une tâche

    tasks = load_tasks()
    task_to_edit = None

    for task in tasks:
        if task["id"] == task_id:
            task_to_edit = task
            break
    # Recherche la tâche à modifier

    if task_to_edit is None:
        return "Tâche introuvable"
        # Si l'ID n'existe pas

    if request.method == "POST":
        # Si le formulaire est envoyé

        task_to_edit["title"] = request.form["title"]
        task_to_edit["description"] = request.form["description"]
        task_to_edit["due_date"] = request.form["due_date"]
        # Met à jour les données

        save_tasks(tasks)

        return redirect(url_for("index"))

    return render_template("edit.html", task=task_to_edit)
    # Sinon → affiche la page de modification


if __name__ == "__main__":
    app.run(debug=True)
    # Lance le serveur Flask (debug = erreurs visibles + reload auto)
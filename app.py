from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

FILE_NAME = "tasks.json"


def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r", encoding="utf-8") as file:
        return json.load(file)


def save_tasks(tasks):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)


@app.route("/")
def index():
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    tasks = load_tasks()

    new_task = {
        "id": len(tasks) + 1,
        "title": request.form["title"],
        "description": request.form["description"],
        "status": "Non faite",
        "due_date": request.form["due_date"]
    }

    tasks.append(new_task)
    save_tasks(tasks)

    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)
    return redirect(url_for("index"))


@app.route("/toggle/<int:task_id>")
def toggle_status(task_id):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            if task["status"] == "Non faite":
                task["status"] = "Faite"
            else:
                task["status"] = "Non faite"
            break

    save_tasks(tasks)
    return redirect(url_for("index"))


@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    tasks = load_tasks()
    task_to_edit = None

    for task in tasks:
        if task["id"] == task_id:
            task_to_edit = task
            break

    if task_to_edit is None:
        return "Tâche introuvable"

    if request.method == "POST":
        task_to_edit["title"] = request.form["title"]
        task_to_edit["description"] = request.form["description"]
        task_to_edit["due_date"] = request.form["due_date"]

        save_tasks(tasks)
        return redirect(url_for("index"))

    return render_template("edit.html", task=task_to_edit)


if __name__ == "__main__":
    app.run(debug=True)
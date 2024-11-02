from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime

app = Flask(__name__)
api = Api(app)

# Data awal tugas (total 2 contoh tugas) dengan detail lebih lengkap
tasks = {
    "1": {
        "title": "Complete the project report",
        "description": "Finish the final report for the project",
        "status": "in-progress",
        "due_date": "2024-11-10"
    },
    "2": {
        "title": "Team meeting",
        "description": "Discuss the project milestones with the team",
        "status": "pending",
        "due_date": "2024-11-12"
    }
}

# Endpoint untuk mengelola tugas
class Task(Resource):
    # GET untuk mengambil data tugas berdasarkan ID
    def get(self, task_id):
        task = tasks.get(task_id)
        if task:
            return jsonify(task)
        return {"message": "Task not found"}, 404

    # PUT untuk memperbarui data tugas berdasarkan ID
    def put(self, task_id):
        if task_id not in tasks:
            return {"message": "Task not found"}, 404
        data = request.get_json()
        tasks[task_id].update(data)
        return jsonify(tasks[task_id])

    # DELETE untuk menghapus data tugas berdasarkan ID
    def delete(self, task_id):
        if task_id in tasks:
            deleted_task = tasks.pop(task_id)
            return {"message": "Task deleted successfully", "task": deleted_task}
        return {"message": "Task not found"}, 404

# Endpoint untuk mengambil semua tugas dan menambahkan tugas baru
class TaskList(Resource):
    # GET untuk mengambil semua tugas
    def get(self):
        return jsonify(tasks)

    # POST untuk menambahkan tugas baru
    def post(self):
        data = request.get_json()
        new_id = str(len(tasks) + 1)
        tasks[new_id] = {
            "title": data["title"],
            "description": data["description"],
            "status": data["status"],
            "due_date": data["due_date"]
        }
        return jsonify(tasks[new_id]), 201

# Menambahkan resource ke dalam API
api.add_resource(TaskList, '/tasks')       # Endpoint untuk semua tugas
api.add_resource(Task, '/tasks/<task_id>') # Endpoint untuk tugas tertentu

# Menjalankan server
if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime

app = Flask(__name__)
api = Api(app)

# Data awal tugas (total 10 tugas dengan detail lebih lengkap)
tasks = {
    "1": {
        "title": "Tugas Matematika",
        "description": "Mengerjakan soal aljabar",
        "due_date": "2024-11-05",
        "status": "Incomplete",
        "priority": "High"
    },
    "2": {
        "title": "Proyek Ilmu Komputer",
        "description": "Membuat program dengan Python",
        "due_date": "2024-11-10",
        "status": "Incomplete",
        "priority": "Medium"
    },
}

# Kelas untuk CRUD tugas
class TaskList(Resource):
    def get(self):
        return {
            "error": False,
            "message": "Success",
            "count": len(tasks),
            "tasks": tasks
        }

class TaskDetail(Resource):
    def get(self, task_id):
        if task_id in tasks:
            return {
                "error": False,
                "message": "Success",
                "task": tasks[task_id]
            }
        return {"error": True, "message": "Data Tidak Ada"}, 404

class AddTask(Resource):
    def post(self):
        data = request.get_json()
        task_id = str(len(tasks) + 1)
        new_task = {
            "title": data.get("title"),
            "description": data.get("description"),
            "due_date": data.get("due_date"),
            "status": data.get("status"),
            "priority": data.get("priority")
        }
        tasks[task_id] = new_task
        return {
            "error": False,
            "message": "Tugas berhasil ditambahkan",
            "task": new_task
        }, 201

class UpdateTask(Resource):
    def put(self, task_id):
        if task_id in tasks:
            data = request.get_json()
            task = tasks[task_id]
            task["title"] = data.get("title", task["title"])
            task["description"] = data.get("description", task["description"])
            task["due_date"] = data.get("due_date", task["due_date"])
            task["status"] = data.get("status", task["status"])
            task["priority"] = data.get("priority", task["priority"])
            return {
                "error": False,
                "message": "Tugas Berhasil di Update",
                "task": task
            }
        return {"error": True, "message": "Task not found"}, 404

class DeleteTask(Resource):
    def delete(self, task_id):
        if task_id in tasks:
            deleted_task = tasks.pop(task_id)
            return {
                "error": False,
                "message": "Task deleted successfully",
                "task": deleted_task
            }
        return {"error": True, "message": "Tugas Tidak ditemukan"}, 404

# Menambahkan endpoint API
api.add_resource(TaskList, '/tasks')
api.add_resource(TaskDetail, '/tasks/<string:task_id>')
api.add_resource(AddTask, '/tasks/add')
api.add_resource(UpdateTask, '/tasks/update/<string:task_id>')
api.add_resource(DeleteTask, '/tasks/delete/<string:task_id>')

if __name__ == '__main__':
    app.run(debug=True)

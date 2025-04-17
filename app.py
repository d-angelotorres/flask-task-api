# app.py
from flask import Flask, jsonify, request
import logging
from pythonjsonlogger import jsonlogger
import uuid
from datetime import datetime

app = Flask(__name__)

# === Structured JSON Logger Setup ===
logger = logging.getLogger("flask-logger")
logger.setLevel(logging.INFO)

# Create formatter and handlers
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(message)s')
log_handler = logging.FileHandler("logs/app.log")  # Inside the app directory
log_handler.setFormatter(formatter)

# Add file handler to logger
logger.addHandler(log_handler)

# Also log to console (for easier debugging during development)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# === Sample Data ===
tasks = [
    {"id": 1, "title": "Learn Flask", "done": False},
    {"id": 2, "title": "Build REST API", "done": False}
]


# === Utility: Generate Context for Logs ===


def log_context(endpoint):
    return {
        "endpoint": endpoint,
        "method": request.method,
        "user_id": str(uuid.uuid4())[:8],
        "timestamp": datetime.utcnow().isoformat()
    }

# === Routes ===


@app.route('/')
def hello():
    logger.info("Accessed root route", extra=log_context("/"))
    return "Welcome to the Task API!"


@app.route('/tasks', methods=['GET'])
def get_tasks():
    logger.info(
        "GET request received",
        extra=log_context("/tasks")
        )
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def create_task():
    logger.info(
        "POST request received",
        extra=log_context("/tasks")
        )
    data = request.get_json()

    if not data or 'title' not in data:
        logger.warning("Missing title in request", extra=log_context("/tasks"))
        return jsonify({'error': 'Title is required'}), 400

    new_task = {
        'id': len(tasks) + 1,
        'title': data['title'],
        'done': False
    }
    tasks.append(new_task)
    logger.info(
        "New task created",
        extra={**log_context("/tasks"), "task": new_task}
        )
    return jsonify(new_task), 201


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    logger.info(
        f"DELETE request received for task {task_id}",
        extra=log_context(f"/tasks/{task_id}")
        )
    task_to_delete = next(
        (task for task in tasks if task['id'] == task_id),
        None
)


    if not task_to_delete:
        logger.warning(
            f"Task {task_id} not found",
            extra=log_context(f"/tasks/{task_id}")
)
        return jsonify({'error': 'Task not found'}), 404

    tasks.remove(task_to_delete)
    logger.info(
        f"Task {task_id} deleted successfully",
        extra=log_context(f"/tasks/{task_id}")
        )
    return jsonify({'message': f'Task {task_id} deleted successfully'})


# === App Runner ===

if __name__ == '__main__':
    logger.info("🚀 Starting Flask server on http://0.0.0.0:5050")
    app.run(debug=True, host='0.0.0.0', port=5050)

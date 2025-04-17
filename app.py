# app.py
from flask import Flask, jsonify, request
import logging
from pythonjsonlogger import jsonlogger
import uuid
from datetime import datetime
import os
import psutil

os.makedirs("logs", exist_ok=True)

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

# === Monitor resources before each request ===
@app.before_request
def log_resource_usage():
    process = psutil.Process()
    cpu = process.cpu_percent(interval=None)
    mem = process.memory_info().rss / (1024 * 1024)  # in MB
    logger.info(f"📊 CPU: {cpu:.2f}% | Memory: {mem:.2f} MB")

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


@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Flask API is running"}), 200


# === Simulate Memory Hog Route ===
@app.route('/memory-hog', methods=['GET'])
def memory_hog():
    logger.info("⚠️ Triggering memory hog...")
    big_data = [x for x in range(10**7)]  # Simulates large memory usage
    return jsonify({"message": "Memory hog simulated"}), 200


# === App Runner ===

if __name__ == '__main__':
    logger.info("🚀 Starting Flask server on http://0.0.0.0:5050")
    app.run(debug=False, host='0.0.0.0', port=5050)

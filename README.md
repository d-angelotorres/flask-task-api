# 🧪 Flask Task API - Final Project Demo

**D'Angelo Torres – CEN 4802C**

A lightweight Flask-based REST API for managing tasks, built and deployed as part of a senior-level Software Integration, Configuration, and Testing course.

---

## 📚 Table of Contents

- [🚀 Project Purpose](#-project-purpose)
- [🛠️ Tech Stack](#️-tech-stack)
- [⚙️ Getting Started](#️-getting-started)
- [🧪 Testing & Stress](#-testing--stress)
- [📈 Monitoring](#-monitoring)
- [🧨 Bonus: Simulating Incidents](#-bonus-simulating-incidents)
- [🐳 Docker](#-docker)
- [🤖 GitHub Actions](#-github-actions)
- [🧠 Reflections](#-reflections)
- [🧾 License](#-license)

---

## 🚀 Project Purpose

This project demonstrates a complete DevOps pipeline, including:

- Automated CI/CD (via GitHub Actions)
- Containerization (via Docker)
- JSON logging with CPU/memory profiling
- Stress testing and monitoring
- Incident simulation (e.g., memory spike)
- Live deployment and debugging strategies

All features are integrated into a working Flask application that supports basic CRUD operations for a to-do list, powered by a REST API.

## 🛠️ Tech Stack

- **Flask** – Web framework
- **Docker** – Containerization
- **GitHub Actions** – CI/CD automation
- **psutil** – Monitoring system performance
- **python-json-logger** – Structured logging
- **requests** – For load/stress testing

---

## ⚙️ Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/d-angelotorres/flask-task-api.git
cd flask-task-api
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app (locally)

```bash
python app.py
```

---

## 🧪 Testing & Stress

Run the included stress test script to simulate heavy traffic:

```bash
python stress_test.py
```

This will send 100 rapid requests to `/tasks` and log response codes.

---

## 📈 Monitoring

Each request logs system stats like CPU and memory usage to `app.log` in JSON format. These logs can be accessed via:

- **Docker Logs**:

  ```bash
  docker logs <container_name>
  ```

- **Mounted Volume**:
  ```bash
  tail -f logs/app.log
  ```

---

## 🧨 Bonus: Simulating Incidents

You can simulate a memory-heavy process by visiting:

```
GET /hog
```

This endpoint creates fake memory usage so you can observe and log spikes.

---

## 🐳 Docker

Build and run the containerized app:

```bash
docker build -t flask-task-api .
docker run -p 5000:5000 flask-task-api
```

Or use a mounted volume to view logs externally:

```bash
docker run -p 5000:5000 -v $(pwd)/logs:/var/log flask-task-api
```

---

## 🤖 GitHub Actions

Every push to `main` triggers:

- Linting
- Build
- `curl` health check to ensure `/tasks` is responding

Broken commits will fail the pipeline. CI ensures only passing builds go through.

---

## 🧠 Reflections

This project was a full-stack ride through real-world DevOps practices, scaled down into a student-sized package. Everything from building and debugging to logging, profiling, and simulating failure was part of the journey — and every step taught something useful.

---

## 🧾 License

MIT License.

---

## 📁 Project Structure

```
.
├── app.py
├── stress_test.py
├── requirements.txt
├── Dockerfile
├── README.md
├── logs/
│   └── app.log
├── .github/
│   └── workflows/
│       └── ci.yml
```

---

⭐ Thanks for checking out the project! Hope it helps or inspires.

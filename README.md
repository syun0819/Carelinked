# FIT5120-TE04-Main-Project


# Project Setup Guide

This repository contains a full-stack application with:

* **Backend:** FastAPI (Python)
* **Frontend:** Vue 3 + Vite (Node.js)

After cloning the repository, follow the steps below to set up the development environment.

---

# 1. Prerequisites

Make sure the following tools are installed on your machine:

| Tool    | Version         |
| ------- | --------------- |
| Python  | 3.12+           |
| Node.js | 18+             |
| npm     | comes with Node |
| Git     | latest          |

Check installations:

```bash
python3 --version
node -v
npm -v
git --version
```

---

# 2. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

---

# 3. Backend Setup (FastAPI)

Navigate to the backend directory:

```bash
cd backend
```

## Create a virtual environment

Mac/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run the backend server

```bash
uvicorn app.main:app --reload
```

The backend will run at:

```
http://localhost:8000
```

API documentation:

```
http://localhost:8000/docs
```

---

# 4. Environment Variables Setup (.env)

For local development, sensitive credentials such as API keys and database access keys are managed through a `.env` file. This file is **never committed to version control**.

## Create the `.env` file

In the project root directory, create a file named `.env`:

```bash
touch .env
```

## Add your environment variables

Open `.env` and add your credentials in the following format:

```
# API Keys
API_KEY=your_api_key_here

# Database
DATABASE_URL=your_database_connection_string_here
```

Replace the placeholder values with your actual keys.

## Load variables in the FastAPI backend

Install `python-dotenv` if it is not already in `requirements.txt`:

```bash
pip install python-dotenv
pip freeze > requirements.txt
```

Then load the variables in your Python code:

```python
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY")
database_url = os.getenv("DATABASE_URL")
```

## Important

* **Never commit `.env` to Git.** It is already listed in `.gitignore`.

---

# 5. Frontend Setup (Vue + Vite)

Open a new terminal and navigate to the frontend folder:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will run at:

```
http://localhost:5173
```

---

# 6. Running the Full Application

Run both services:

| Service  | Command                           | URL                   |
| -------- | --------------------------------- | --------------------- |
| Backend  | `uvicorn app.main:app --reload` | http://localhost:8000 |
| Frontend | `npm run dev`                   | http://localhost:5173 |

The Vue frontend communicates with the FastAPI backend via API requests.

---

# 7. Project Structure

```
project-root
│
├── backend
│   ├── app
│   │   └── main.py
│   ├── requirements.txt
│   └── venv
│
├── frontend
│   ├── src
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── README.md
├── .env

```

---

# 8. Installing New Backend Dependencies

If new Python packages are added:

```bash
pip install <package>
pip freeze > requirements.txt
```

Commit the updated `requirements.txt`.

---

# 9. Installing New Frontend Dependencies

```bash
npm install <package>
```

Commit the updated `package.json` and `package-lock.json`.

---

# 10. Important Notes

* **Never work directly on the `main` branch.** Always create and work on a feature or bugfix branch (see Section 12).
* Always activate the Python virtual environment before running backend commands.
* Run backend and frontend in **separate terminals**.
* Do not commit the following folders:

```
venv/
node_modules/
dist/
```

These are already included in `.gitignore`.

---

# 11. Troubleshooting

### Backend won't start

Ensure the virtual environment is activated and dependencies are installed.

### Frontend won't start

Run:

```bash
npm install
```

to install missing dependencies.

---

# 12. Development Workflow

> **Important:** Never commit directly to `main`. Always work on a separate branch.

Typical workflow:

1. Pull latest changes from `main`

```bash
git checkout main
git pull
```

2. Create and switch to a new branch

```bash
git checkout -b feature/your-feature-name
```

Use a descriptive branch name, for example:

- `feature/add-login-page`
- `bugfix/fix-api-error`

3. Start backend

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

4. Start frontend

```bash
cd frontend
npm run dev
```

5. Commit and push your branch

```bash
git add .
git commit -m "describe your changes"
git push origin feature/your-feature-name
```

Then open a Pull Request to merge into `main`.

---

```

```

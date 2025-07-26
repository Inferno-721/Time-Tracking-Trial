# Time Tracking Trial

A full-stack time tracking application with:
- **Backend**: FastAPI (Python)
- **Frontend**: Vite + React (JavaScript/TypeScript)
- **Local App**: Python (for local system integration)

## Project Structure

```
Time Tracking Trial/
├── backend/      # FastAPI backend (API, DB, Alembic)
├── frontend/     # Vite + React frontend
├── local-app/    # Python local app (system integration)
├── run_all.sh    # Script to run all services (Linux/macOS)
├── .gitignore
├── README.md
└── project-plan.md
```

## Prerequisites
- Python 3.10+
- Node.js (v18+ recommended)
- npm

---

## Backend (FastAPI)

1. **Setup virtual environment:**
   ```sh
   cd backend
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   # or
   source venv/bin/activate      # On Linux/macOS
   pip install -r requirements.txt
   ```
2. **Run database migrations:**
   ```sh
   alembic upgrade head
   ```
3. **Start backend server:**
   ```sh
   uvicorn app:app --reload
   ```
   The API will be available at [http://localhost:8000](http://localhost:8000)

---

## Frontend (Vite + React)

1. **Install dependencies:**
   ```sh
   cd frontend
   npm install
   ```
2. **Start development server:**
   ```sh
   npm run dev
   ```
   The app will be available at [http://localhost:5173](http://localhost:5173)

---

## Local App (Python)

1. **Setup virtual environment:**
   ```sh
   cd local-app
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   # or
   source venv/bin/activate      # On Linux/macOS
   pip install -r requirements.txt
   ```
2. **Run the local app:**
   ```sh
   python main.py
   ```

---

## Run All Services (Linux/macOS)

You can use the provided script to start all services:
```sh
./run_all.sh
```

---

## Project Plan
See `project-plan.md` for a high-level overview and planning notes.

---

## License
Specify your license here.

time-tracking-trial/
│
├── backend/
│   ├── app.py                # FastAPI app entrypoint
│   ├── models.py             # SQLAlchemy models (Employee, Project, Task, TimeLog, Screenshot)
│   ├── schemas.py            # Pydantic schemas for API
│   ├── crud.py               # DB operations
│   ├── api/
│   │   ├── employee.py       # Employee API endpoints
│   │   ├── project.py        # Project API endpoints
│   │   ├── task.py           # Task API endpoints
│   │   ├── time.py           # Time Tracking API endpoints
│   │   └── screenshot.py     # Screenshot API endpoints
│   ├── database.py           # DB connection/session
│   └── requirements.txt      # Backend dependencies
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   ├── Onboard.tsx
│   │   │   └── Download.tsx
│   │   └── api.ts            # API calls
│   ├── package.json
│   └── README.md
│
├── local-app/
│   ├── main.py               # Entry point (PyQt5 or Tkinter)
│   ├── ui.py                 # UI logic
│   ├── api.py                # Communicate with backend
│   ├── screenshot.py         # Screenshot logic
│   ├── background.py         # IP/MAC collection
│   └── requirements.txt
│
└── README.md

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, crud, models
from database import SessionLocal
from passlib.context import CryptContext  # ✅ Add this

# ✅ Create pwd_context instance
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.EmployeeOut)
def add_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = crud.get_employee_by_email(db, email=employee.email)
    if db_employee:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_employee(db=db, employee=employee)

@router.post("/login")
def login_employee(data: schemas.LoginRequest, db: Session = Depends(get_db)):
    emp = crud.get_employee_by_email(db, email=data.email)
    if not emp or not pwd_context.verify(data.password, emp.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"id": emp.id, "name": emp.name, "email": emp.email}

@router.get("/{employee_id}", response_model=schemas.EmployeeOut)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

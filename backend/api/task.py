from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, crud
from database import SessionLocal
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.TaskOut)
def add_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task)

@router.get("/", response_model=List[schemas.TaskOut])
def get_tasks(db: Session = Depends(get_db)):
    return crud.get_all_tasks(db=db)

@router.get("/project/{project_id}", response_model=List[schemas.TaskOut])
def get_tasks_by_project(project_id: int, db: Session = Depends(get_db)):
    return crud.get_tasks_by_project(db=db, project_id=project_id)

@router.get("/{task_id}", response_model=schemas.TaskOut)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(crud.models.Task).filter(crud.models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task 
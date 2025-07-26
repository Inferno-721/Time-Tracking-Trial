from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, crud
from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.TimeLogOut)
def log_time(time_log: schemas.TimeLogCreate, db: Session = Depends(get_db)):
    return crud.create_time_log(db=db, time_log=time_log)

@router.get("/{time_log_id}", response_model=schemas.TimeLogOut)
def read_time_log(time_log_id: int, db: Session = Depends(get_db)):
    db_time_log = db.query(crud.models.TimeLog).filter(crud.models.TimeLog.id == time_log_id).first()
    if db_time_log is None:
        raise HTTPException(status_code=404, detail="Time log not found")
    return db_time_log 
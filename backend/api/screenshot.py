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

@router.post("/", response_model=schemas.ScreenshotOut)
def upload_screenshot(screenshot: schemas.ScreenshotCreate, db: Session = Depends(get_db)):
    return crud.create_screenshot(db=db, screenshot=screenshot)

@router.get("/{screenshot_id}", response_model=schemas.ScreenshotOut)
def read_screenshot(screenshot_id: int, db: Session = Depends(get_db)):
    db_screenshot = db.query(crud.models.Screenshot).filter(crud.models.Screenshot.id == screenshot_id).first()
    if db_screenshot is None:
        raise HTTPException(status_code=404, detail="Screenshot not found")
    return db_screenshot 
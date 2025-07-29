from sqlalchemy.orm import Session
import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def create_employee(db: Session, employee: schemas.EmployeeCreate):
    db_employee = models.Employee(
        email=employee.email,
        name=employee.name,
        hashed_password=get_password_hash(employee.password)
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def get_employee(db: Session, employee_id: int):
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()

def get_employee_by_email(db: Session, email: str):
    return db.query(models.Employee).filter(models.Employee.email == email).first()

def create_project(db: Session, project: schemas.ProjectCreate):
    db_project = models.Project(name=project.name)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def get_all_projects(db: Session):
    return db.query(models.Project).all()

def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(name=task.name, project_id=task.project_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_all_tasks(db: Session):
    return db.query(models.Task).all()

def get_tasks_by_project(db: Session, project_id: int):
    return db.query(models.Task).filter(models.Task.project_id == project_id).all()

def create_time_log(db: Session, time_log: schemas.TimeLogCreate):
    db_time_log = models.TimeLog(
        employee_id=time_log.employee_id,
        task_id=time_log.task_id,
        start_time=time_log.start_time,
        end_time=time_log.end_time,
        ip=time_log.ip,
        mac=time_log.mac
    )
    db.add(db_time_log)
    db.commit()
    db.refresh(db_time_log)
    return db_time_log

import base64

def create_screenshot(db: Session, screenshot: schemas.ScreenshotCreate):
    db_screenshot = models.Screenshot(
        employee_id=screenshot.employee_id,
        timestamp=screenshot.timestamp,
        image_data=base64.b64decode(screenshot.image_data),  # decode here!
        permission_flag=screenshot.permission_flag
    )
    db.add(db_screenshot)
    db.commit()
    db.refresh(db_screenshot)
    return db_screenshot
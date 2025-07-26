from pydantic import BaseModel, EmailStr
from typing import Optional, List
import datetime

class EmployeeBase(BaseModel):
    email: EmailStr
    name: str

class EmployeeCreate(EmployeeBase):
    password: str

class EmployeeOut(EmployeeBase):
    id: int
    is_active: bool
    class Config:
        orm_mode = True

class ProjectBase(BaseModel):
    name: str

class ProjectCreate(ProjectBase):
    pass

class ProjectOut(ProjectBase):
    id: int
    class Config:
        orm_mode = True

class TaskBase(BaseModel):
    name: str
    project_id: int

class TaskCreate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: int
    class Config:
        orm_mode = True

class TimeLogBase(BaseModel):
    employee_id: int
    task_id: int
    start_time: datetime.datetime
    end_time: Optional[datetime.datetime] = None
    ip: Optional[str] = None
    mac: Optional[str] = None

class TimeLogCreate(TimeLogBase):
    pass

class TimeLogOut(TimeLogBase):
    id: int
    class Config:
        orm_mode = True

class ScreenshotBase(BaseModel):
    employee_id: int
    timestamp: datetime.datetime
    permission_flag: bool

class ScreenshotCreate(ScreenshotBase):
    image_data: str

class ScreenshotOut(ScreenshotBase):
    id: int
    class Config:
        orm_mode = True
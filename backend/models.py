from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, LargeBinary
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    hashed_password = Column(String, nullable=False)
    # Relationships
    time_logs = relationship("TimeLog", back_populates="employee")
    screenshots = relationship("Screenshot", back_populates="employee")

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    # Relationships
    tasks = relationship("Task", back_populates="project")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="tasks")
    # Relationships
    time_logs = relationship("TimeLog", back_populates="task")

class TimeLog(Base):
    __tablename__ = "timelogs"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    task_id = Column(Integer, ForeignKey("tasks.id"))
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    ip = Column(String, nullable=True)   # <-- add this
    mac = Column(String, nullable=True)  # <-- add this
    # Relationships
    employee = relationship("Employee", back_populates="time_logs")
    task = relationship("Task", back_populates="time_logs")

class Screenshot(Base):
    __tablename__ = "screenshots"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    image_data = Column(LargeBinary)
    permission_flag = Column(Boolean, default=True)
    # Relationships
    employee = relationship("Employee", back_populates="screenshots")
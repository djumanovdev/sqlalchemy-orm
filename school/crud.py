from datetime import datetime
from sqlalchemy import or_, not_, and_
from .models import Student
from .db import get_db


def create_student(first_name: str, last_name: str, birthdate: datetime, bio: str | None = None):
    student = Student(
        first_name=first_name,
        last_name=last_name,
        birthdate=birthdate,
        bio=bio
    )
    
    with get_db() as session:
        session.add(student)
        session.commit()

def get_students() -> list[Student]:
    with get_db() as session:
        students = session.query(Student).all()
    
    return students

def get_one_student(student_id: int) -> Student | None:
    with get_db() as session:
        student = session.query(Student).get(student_id)
    
    return student

def search_students_by_first_name(first_name: str) -> list[Student]:
    with get_db() as session:
        students = session.query(Student).filter(Student.first_name==first_name).all()
    
    return students

def search_students_by_name(name: str) -> list[Student]:
    with get_db() as session:
        students = session.query(Student).filter(
            or_(Student.first_name.like(f'%{name}%'), Student.last_name.like(f'%{name}%'))
        ).all()
    
    return students

def update_student(
    student_id: int | None = None,
    first_name: str | None = None, 
    last_name: str | None = None, 
    birthdate: datetime | None = None, 
    bio: str | None = None
):
    student = get_one_student(student_id)

    if student:
        with get_db() as session:
            student.first_name = first_name if first_name else student.first_name
            student.last_name = last_name if last_name else student.last_name
            student.birthdate = birthdate if birthdate else student.birthdate
            student.bio = bio if bio else student.bio

            session.add(student)
            session.commit()

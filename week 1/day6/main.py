
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel    

app = FastAPI()


class Student(BaseModel):
    id: int
    name: str
    course: str


students = [
    Student(id=1, name="Aarav", course="AI Engineering"),
    Student(id=2, name="Priya", course="Python"),
    Student(id=3, name="Rohan", course="Data Science"),
]


@app.get("/")
def home():
    return {"message": "Welcome to my first API!"}


@app.get("/hello")
def say_hello(name: str = "Student"):
    return {"message": f"Hello, {name}!"}


@app.get("/students")
def get_students():
    return students


@app.get("/students/{student_id}")
def get_student(student_id: int):
    for student in students:
        if student.id == student_id:
            return student
    raise HTTPException(status_code=404, detail="Student not found")




@app.post("/students", status_code=201)
def add_student(student: Student):
    for existing_student in students:
        if existing_student.id == student.id:
            raise HTTPException(
                status_code=409,
                detail="Student with this ID already exists"
            )

    students.append(student)
    return {
        "message": "Student added successfully",
        "student": student,
    }
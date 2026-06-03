from fastapi import FastAPI
from pydantic import BaseModel
import json
import os

app = FastAPI()
DATA_FILE = "courses.json"

# 과목 저장을 위한 Pydantic 모델
class Course(BaseModel):
    id: int
    title: str
    instructor: str

# 서버가 켜질 때 초기 JSON 파일이 없으면 빈 배열([]) 생성
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

@app.get("/")
def read_root():
    return {"message": "FastAPI Docker Container가 성공적으로 구동 중입니다!"}

# [과제 요구사항] GET /courses 구현
@app.get("/courses")
def get_courses():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# [과제 요구사항] POST /courses 구현
@app.post("/courses")
def create_course(course: Course):
    with open(DATA_FILE, "r") as f:
        courses = json.load(f)
    
    courses.append(course.model_dump())
    
    with open(DATA_FILE, "w") as f:
        json.dump(courses, f, indent=4)
        
    return {"message": "과목이 성공적으로 등록되었습니다.", "course": course}
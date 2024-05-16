# from fastapi import FastAPI

# app = FastAPI()

# @app.get('/')
# def read_root():
#   return {"Hello" : "World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str = None):
#   return {"item_id" : item_id, "q" : q}

# # /products/<int:item_id>/

# @app.get('/like/lion')
# def response_lion():
#   return {"응답" : "멋쨍이 사자!"}


# CRUD (Create, Read, Update, Delete) by FastAPI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
  name : str
  description: str = None
  price : float
  tax : float = None

@app.post('/items/')
def create_item(item : Item):
  return {"name" : item.name, "price" : item.price}

@app.get('/items/{item_id}')
def read_item(item_id : int):
  return {"item_id" : item_id, "name" : "Sample Item"}

@app.put('/items/{item_id}')
def update_item(item_id : int, item : Item):
  return {"item_id" : item_id, 'name' : Item.name, "price" : Item.price}

@app.delete('/items/{item_id}')
def delete_item(item_id : int):
  return {"message" : "Item deleted"}


### 연습문제 
# 1. 학생 정보 조회 
# "/likelion/{student_id}" 경로를 GET 메서드로 설정하고, 
# 요청된 student_id에 대응하는 멋쟁이사자처럼 학원의 학생 정보를 반환하는 엔드포인트
# 학생 정보는 JSON 객체로, 학생의 이름과 이메일을 포함
# 이때, 각 student_id에 따라 하드코딩된 데이터를 제공
@app.get('/likelion/{student_id}')
def read_student(student_id : int):
  student_data = {
        1: {"name": "김멋사", "email": "kimmutsa@example.com"},
        2: {"name": "이멋사", "email": "leemutsa@example.com"} 
  }
  student_info = student_data.get(student_id, {"message": "Student not found"})
  return student_info


# 2. 프로젝트 아이템 등록
# "/projects/" 경로에 POST 메서드를 사용하여, 
# 멋쟁이사자처럼 학생들이 진행하는 프로젝트 아이템 정보를 받아 새로운 프로젝트를 등록하는 엔드포인트
# 요청 본문으로는 Item 모델을 활용하며, 프로젝트의 이름과 짧은 설명을 반환
@app.post('/projects/')
def create_project(item: Item):
  return {'name' : item.name, 'description' : item.description}

# 3. 프로젝트 아이템 삭제
# "/projects/{project_id}" 경로에 DELETE 메서드를 사용하여,
# 요청된 project_id에 해당하는 프로젝트 아이템을 삭제하는 엔드포인트
# 삭제가 성공시, "Project deleted successfully" 메시지 반환
@app.delete('/projects/{project_id}')
def delete_project(project_id : int):
  return {"message" : "Project deleted successfully"} 
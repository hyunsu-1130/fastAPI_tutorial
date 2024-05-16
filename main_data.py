# Pydantic을 사용한 데이터 검증
# 데이터 유효성 검사는 사용자 입력이나 외부 데이터 소스에서 오는 데이터가 예상한 형식과 규칙을 따르는지 확인하는 과정 
# -> 애플리케이션에서 처리하는 데이터의 정확성과 신뢰성 보장

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, ValidationError

app = FastAPI()

class User(BaseModel):
    name: str
    email: EmailStr   # EmailStr은 Pydantic에서 제공하는 이메일 타입으로, 유효한 이메일 주소인지 자동으로 검증
    age: int

@app.post("/register/")
def register_user(user: User):
    if user.age < 18:
        raise HTTPException(status_code=400, detail="Age must be 18 or over.")
    return {"name": user.name, "email": user.email, "age": user.age}


from datetime import datetime

class Product(BaseModel):
    name: str
    price: float
    release_date: datetime

@app.post("/product/")
def add_product(product: Product):
    return {"name": product.name, "price": product.price, "release_date": product.release_date}


### 연습문제
# 1. 대학 행사 등록
# 대학에서 주최하는 이벤트를 등록하기 위한 API 엔드포인트
# 이벤트 이름, 날짜(`datetime`), 참가자 수(`int`)를 입력받아 등록하는 기능 구현
class Event(BaseModel):
    name : str
    date : datetime     # ex) "date": "2024-05-18T12:30:00.0Z"
    num_of_participants : int

@app.post('/event/')
def create_event(event : Event):
  return {"message" : '이벤트 등록 완료', 'event' : event}

# 2. 도서 대출 기록
# 학교 도서관의 도서 대출 기록을 관리하는 API
# 도서의 제목(`str`), 저자(`str`), 대출 날짜(`date`)를 입력받아 기록
from datetime import date

class BookLoan(BaseModel):
  title : str
  writer : str
  loan_date : date

@app.post('/loan/')
def lend_book(bookloan : BookLoan):
    return {"message" : "대출이 완료되었습니다." , 'bookloan' : bookloan}


# 3. 멋쟁이사자처럼 회원 등록
# 멋쟁이사자처럼 클럽의 새 회원을 등록하는 API
# 회원의 이름(`str`), 이메일(`EmailStr`), 등록 날짜(`date`)를 입력받아 등록
class Member(BaseModel):
  name : str
  email : EmailStr
  registration_date : date

@app.post('/lion/')
def add_new_mem(member : Member):
   return {"message" : f"{member.name}님, 멋사 회원이 되신것을 환영합니다." , 'member' : member}

# 4. 학식 메뉴 등록
# 학교 식당에서 제공하는 메뉴를 등록하는 API
# 메뉴 이름(`str`), 가격(`float`), 제공 날짜(`date`)를 입력받아 등록
class Menu(BaseModel):
   name : str
   price : float
   provided_date : date

@app.post('/lunch/')
def add_menu(menu : Menu):
   return {"message" : f"{menu.name} 메뉴 등록이 완료되었습니다." , 'menu' : menu}


# 5. 스터디 그룹 생성
# 학생들이 스터디 그룹을 만들 때 사용할 수 있는 API
# 스터디 그룹의 이름(`str`), 주제(`str`), 최대 인원 수(`int`)를 입력받아 생성
class Study(BaseModel):
   name : str
   topic : str
   max_num : int

@app.post('/study/')
def add_study(study : Study):
   return {"message" : "스터디 그룹 등록이 완료되었습니다." , 'study' : study}


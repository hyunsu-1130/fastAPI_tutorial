from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
  name : str
  age : int

# 사용자 정의 응답 (Response 모델)
@app.get("/user/{user_id}", response_model=User)
def get_user(user_id : int):
    # 실제 구현에서는 데이터베이스에서 사용자 정보를 조회하겠지만, 여기서는 예시 데이터를 사용합니다.
    return User(name="Alice", age=30)
    
    # return {"name":"Alice", "age":30, "more":"good"} # response_model=User를 없애야 테이블외의 내용도 출력됨 !!

# 상태 코드 설정 및 처리
from fastapi import FastAPI, status

app = FastAPI()

@app.post("/create_user", status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    # 사용자 생성 로직 (가정)
    return {"message": "User created successfully", "user": user}


#### 연습문제
# 1. 기본 GET 엔드포인트 생성
# "/hello" 경로에 GET 요청을 처리하는 엔드포인트를 만들고, "Hello, LikeLion!"이라는 메시지 반환
@app.get('/hello')
def read_hello():
   return {"message" : "Hello, LikeLion!"}

# 2. 간단한 사용자 정보 반환
# "/user/{user_id}" 경로, 사용자 ID를 입력받아 해당 사용자의 이름과 이메일을 반환하는 엔드포인트
@app.get('/user/{user_id}')
def read_user(user_id : int):
   return {"name" : 'name', "email" : "email"}

# 3. POST 요청 처리
# 새로운 학생 정보를 입력받아 저장하는 "/students" 경로의 POST 엔드포인트 (학생 정보에는 `name`과 `email`이 포함)
@app.post('/students')
def create_student(name : str, email : str):
   return {"name" : name, "email" : email}

# 4. 항목 삭제
# 특정 항목 ID를 입력받아 해당 항목을 삭제하는 "/items/{item_id}" 경로의 DELETE 요청 엔드포인트
@app.delete('/items/{item_id}')
def delete_item(item_id : int):
   return {"message" : "deleted item"}

# 5. 조건부 응답
# 사용자의 연령에 따라 다른 메시지를 반환하는 "/age/{age}" 경로의 GET 요청 엔드포인트
@app.get("/age/{age}")
def read_by_age(age : int):
   if age < 18:
    return {"message" : "미성년자"}
   else :
      return {"message" : "성인"}
   

class Student:
   def __init__(self, name: str, email : str):
      self.name = name
      self.email = email
students = []
   
# 6. 상태 코드 반환
# 학생 정보 생성 시, HTTP 상태 코드 201을 반환하는 "/create_student" 경로의 POST 엔드포인트
@app.post('/create_student', status_code=status.HTTP_201_CREATED)
def create_new_student(student : Student):
   return {"message": "Student created successfully", "student": student}

# 7. 리스트 반환
# 모든 학생의 목록을 반환하는 "/students" 경로의 GET 요청 엔드포인트
@app.get("/all_students")
def read_all_students():
  return {"students" : students}


# 8. 응답 모델 사용
# Pydantic을 사용하여 사용자 정보 응답 모델 정의, 이를 사용하여 사용자 정보를 반환하는 GET 엔드포인트
# Pydantic을 사용하여 사용자 정보 응답 모델 정의
class UserInfo(BaseModel):
   name : str
   age : int

users = [
   UserInfo(name='John', age=20),
   UserInfo(name='Alice', age=24)
]

@app.get('/new_users/{user_id}', response_model=UserInfo)
def read_new_user(user_id : int):
  if user_id < 0 or user_id >= len(users):
        return {"message": "User not found"}
  return users[user_id]


# 9. 경로 파라미터와 쿼리 파라미터 조합
# "/search" 경로에서 쿼리 파라미터로 입력받은 검색 키워드를 통해 해당하는 정보를 반환하는 GET 요청 엔드포인트
db = {
   'apple' : {'color' : 'red', 'taste' : 'sweet'},
   'banana' : {'color' : 'yellow', 'taste' : 'sweet'},
   "carrot": {"color": "orange", "taste": "crunchy"},
}

@app.get('/search')
def search_item(keyword : str):
   if keyword in db:
      return {'result':db[keyword]}
   else :
      return {'message' : '해당 키워드의 아이템이 없습니다.'}
   
   # http://localhost:8000/search?keyword=apple <- '?' 쿼리 파라미터


from fastapi import Query
# 추가로 키워드 외에 정보로도 값을 찾기
@app.get("/search_by_info")
def search_item(color : str = Query(None), taste: str = Query(None)) :
    results = []
    for item_name, item_info in db.items():   # db의 각 아이템에 대해 이름과 정보 쌍을 순회 , 딕셔너리의 items() 메서드를 사용
        # item_name :  항목의 이름 / item_info : 해당 항목의 정보
        if (color and item_info.get("color") == color) or (taste and item_info.get("taste") == taste):
            results.append(item_name)
    if results:
        return {"result": results}
    else:
        return {"message": "입력하신 특성에 해당하는 아이템이 없습니다."}
    

# 10. 커스텀 상태 코드와 에러 메시지
# 잘못된 요청에 대해 400 상태 코드와 함께 "Invalid request"라는 에러 메시지를 반환하는 엔드포인트
# raise HTTPException(status_code=…, detail=…)
from fastapi.exceptions import HTTPException
@app.get('/invalid request')
def invalid_request():
  raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request")


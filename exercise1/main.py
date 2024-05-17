# main.py
from fastapi import FastAPI, Depends, HTTPException
from typing import List
from database import get_db, engine
from .models import Base, User as UserModel
from .schemas import UserCreate, UserUpdate, User
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

@asynccontextmanager      # 비동기 컨텍스트 관리자 정의
async def lifespan(app: FastAPI):     
    async with engine.begin() as conn:    # 비동기 컨텍스트 시작
        # 데이터베이스 테이블 생성
        await conn.run_sync(Base.metadata.create_all)     # 모든 DB 테이블 생성
    
    try:
        yield  # 여기에서 FastAPI 앱이 실행되는 동안 컨텍스트를 유지합니다.
    finally:
        # 비동기 데이터베이스 연결 종료
        await engine.dispose()
        
app = FastAPI(lifespan=lifespan)

# @app.on_event("startup")
# async def startup_event():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

@app.post("/users/", response_model=User)   # 새로운 사용자 추가
async def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    new_user = UserModel(**user_data.model_dump())
    db.add(new_user)    # 새 제품 추가 및 커밋
    await db.commit()
    await db.refresh(new_user)
    return new_user


@app.get("/users/", response_model=List[User])    # 사용자 목록을 나타내는 리스트 반환
async def list_users(db: Session = Depends(get_db)):
    result = await db.execute(select(UserModel))   # await 키워드 = 비동기적 실행
    users = result.scalars().all()   # 결과 집합을 각 행의 스칼라 값으로 반환 및 모든 행 리스트로 반환
    return users
    

@app.get("/users/{user_id}", response_model=User)   # 사용자 아이디에 해당하는 사용자 값 반환
async def read_user(user_id: int, db: Session = Depends(get_db)):
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = result.scalars().first()
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{user_id}", response_model=User)       # 사용자 정보 수정
async def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    user = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = user.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user_data.dict(exclude_unset=True).items():
        setattr(user, key, value)
    await db.commit()
    await db.refresh(user)
    return user


@app.delete("/users/{user_id}", status_code=204)    # 사용자 삭제
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = user.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    await db.commit()
    return {"message": "User deleted successfully"}

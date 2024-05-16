# main.py
from fastapi import FastAPI, Depends, HTTPException
from typing import List
from database import get_db, engine
from models import Base, Product as ProductModel
from schemas import ProductCreate, Product, ProductUpdate
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

@app.get("/products/", response_model=List[Product])    # 제품목록을 나타내는 리스트 반환
async def read_products(db: Session = Depends(get_db)):
    result = await db.execute(select(ProductModel))   # await 키워드 = 비동기적 실행
    products = result.scalars().all()   # 결과 집합을 각 행의 스칼라 값으로 반환 및 모든 행 리스트로 반환
    return products
    
@app.post("/products/", response_model=Product)   # 새 제품 생성
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = ProductModel(**product.model_dump())
    db.add(db_product)    # 새 제품 추가 및 커밋
    await db.commit()
    await db.refresh(db_product)
    return db_product

@app.get("/products/{product_id}", response_model=Product)
async def read_product(product_id: int, db: Session = Depends(get_db)):
    result = await db.execute(select(ProductModel).where(ProductModel.id == product_id))
    product = result.scalars().first()
    if product:
        return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = await db.execute(select(ProductModel).where(ProductModel.id == product_id))
    db_product = db_product.scalars().first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    for var, value in product.dict(exclude_unset=True).items():
        setattr(db_product, var, value)
    await db.commit()
    await db.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}", status_code=204)
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = await db.execute(select(ProductModel).where(ProductModel.id == product_id))
    db_product = db_product.scalars().first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    await db.delete(db_product)
    await db.commit()
    return {"ok": True}

# 데이터 모델 정의
from pydantic import BaseModel

class ProductBase(BaseModel):   # 모든 제품에 대한 기본적인 정보를 정의
    name: str
    description: str = None
    price: float

class ProductCreate(ProductBase):       # 제품 생성
    pass

class ProductUpdate(ProductBase):       # 제품 수정
    pass

class Product(ProductBase):         #  제품의 전체 정보
    id: int

    class Config:
        orm_mode = True

        # orm_mode = True가 사용되는 구체적인 부분 및 이유
        # FastAPI 앱의 라우터 함수에서 DB로부터 쿼리된 결과를 반환할 때,
        # -> SQLAlchemy ORM이 반환한 모델 객체를 Pydantic 모델로 자동 변환 

        # ex ) response_model=List[Product]
        # FastAPI는 이를 Product Pydantic 모델로 자동 변환하는데, 이때 orm_mode = True가 설정되어 있다면
        # Product 클래스를 사용하여 SQLAlchemy 모델과 Pydantic 모델 간의 호환성을 보장








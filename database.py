import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL, echo=True)   #  비동기 엔진
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

async def get_db():     # DB 세션을 비동기로 반환
    async with SessionLocal() as session:
        yield session    
        # yield : 제너레이터(generator)를 만들 때 사용되는 키워드
        # 제너레이터는 값을 하나씩 생성하는 이터레이터(iterator)를 생성하는데 사용
        # 이터레이터를 통해 값을 한 번에 모두 메모리에 저장하지 않고, 필요할 때마다 값을 생성
        # yield는 함수 내부에서 값을 반환하지만, 함수의 상태를 보존하고 다음 호출 시에 이어서 실행할 수 있음

          # yield는 함수를 일시 중지하고 값을 반환할 수 있는 특별한 키워드
          # 이터레이터로 동작하는 함수를 만들 때 사용되는데, 
          # 함수 실행 중에 yield를 만나면 함수는 그 자리에서 멈춰서 값을 반환하고,
          # 다음에 호출될 때는 그 다음 코드부터 실행
          # 이런 식으로 함수의 상태를 유지하면서 값을 생성함
          # 예를 들어, count()라는 함수가 있고 이 함수를 호출하면 1부터 3까지의 값을 생성하는데, 
          # yield를 사용해서 하나씩 값을 반환할 수 있어.


          # def count():
          #     yield 1
          #     yield 2
          #     yield 3

          # # 제너레이터 함수 호출
          # gen = count()

          # # 제너레이터 객체를 이터레이션하여 값에 접근
          # print(next(gen))  # 1
          # print(next(gen))  # 2
          # print(next(gen))  # 3
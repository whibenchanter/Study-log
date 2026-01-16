### blocking.py ### 
#    (개념설명용)
# FASTAPI는 왜 빠를까?

import asyncio
import time

async def async_sleep(): # 양보, 코루틴함수(협동함수, 자녀)
    await asyncio.sleep(3)

async def blocking_sleep(): # 양보 못하게 막음
    time.sleep(3)

async def main():

    coro1 = async_sleep()
    coro2 = async_sleep()

    await asyncio.gather(coro1, coro2) #여러작업 묶어주는 도구

asyncio.run(main()) 
# 이벤트루프(순서관리자, 엄마) 
# 실행 중(한번에 1개씩, line23), 
# 대기 중(I/O 작업 중, line10),  
# 준비 중(I/O 작업완료 이후, line10에서 3초 지난 이후)











### model.py ###
# 모델링(설계도)
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Item(Base):
    __tablename__ = "items"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)











### 1-16.connection_async.py ###
# (국토교통부에서 관리하는 고속도로 생성 = 연결 + 관리)

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# 주소
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# 편도 = 주소로 가는 길
engine = create_async_engine(DATABASE_URL)

# 세션공장(설계도) (* 세션(Session) = DB 연결 및 도로관리차량)
AsyncSessionFactory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

# DB 연결 및 도로관리차량투입 및 해제 
async def get_async_session(): # 투입할 애들 만들기
    async with AsyncSessionFactory() as session:
        yield session # 관리 끝나면 실행 = 연결 해제









### 1-16.crud_async.py ### 
#          (실행부)

from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy import select

from connection_async import AsyncSessionFactory, get_async_session
# 위의 파일 연결하는 코드
from model import Item
# 위의 파일 연결하는 코드2

app = FastAPI()

class ItemResponse(BaseModel):
    id: int
    name: str
    price: int

# C: 상품 등록 API
class ItemCreateRequest(BaseModel):
    name: str
    price: int

#의존성 주입(Dependency Injection) 적용한 버전
@app.post("/items", status_code=201)
async def create_item_api(
    body: ItemCreateRequest,
    session: AsyncSession = Depends(get_async_session), # get_async_session 주입
) -> ItemResponse:
    new_item = Item(name=body.name, price=body.price)
    session.add(new_item)  # DB에 저장할 애들을 선별
    await session.commit()  # DB에 반영
    return new_item

# R: 전체 상품 조회 API
@app.get("/items", status_code=200)
async def get_items_api() -> list[ItemResponse]:
    async with AsyncSessionFactory() as session:
        stmt = select(Item)  # statement = SQL 구문
        result = await session.execute(stmt)  # 1) DB 조회
        items : list[Item]= result.scalars().all()  # 2) Item 객체로 변환
        return items

# R: 단일 상품 조회 API
@app.get("/items/{item_id}", status_code=200)
async def get_item_api(item_id: int) -> ItemResponse:
    async with AsyncSessionFactory() as session:
        stmt = select(Item).where(Item.id == item_id)
        result = await session.execute(stmt)
        item: Item | None = result.scalar()
        
        if item is None:
            raise HTTPException(
                status_code=404, detail=f"Item Not Found(id: {item_id})",
            )
        return item

# U: 상품 수정 API (PATCH)
class ItemUpdateRequest(BaseModel):
    name: str | None = None
    price: int | None = None

@app.patch("/items/{item_id}", status_code=200)
async def update_item_api(item_id: int, body: ItemUpdateRequest) -> ItemResponse:
    async with AsyncSessionFactory() as session:
        stmt = select(Item).where(Item.id == item_id)
        result = await session.execute(stmt)
        item: Item | None = result.scalar()
        
        if item is None:
            raise HTTPException(
                status_code=404, detail=f"Item Not Found(id: {item_id})",
            )
        
        if body.name:
            item.name = body.name
        if body.price:
            item.price = body.price
        
        await session.commit()
        return item

# U: 상품 수정 API (PUT)
class ItemReplaceUpdate(BaseModel):
    name: str
    price: int

@app.put("/items/{item_id}", status_code=200)
async def replace_item_api(item_id: int, body: ItemReplaceUpdate) -> ItemResponse:
    async with AsyncSessionFactory() as session:
        stmt = select(Item).where(Item.id == item_id)
        result = await session.execute(stmt)
        item: Item | None = result.scalar()
        
        if item is None:
            raise HTTPException(
                status_code=404, detail=f"Item Not Found(id: {item_id})",
            )
        
        item.name = body.name
        item.price = body.price
        
        await session.commit()
        await session.refresh(item)
        return item


# D: 상품 삭제 API
@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item_api(item_id: int) -> None:
    async with AsyncSessionFactory() as session:
        stmt = select(Item).where(Item.id == item_id)
        result = await session.execute(stmt)
        item: Item | None = result.scalar()
        
        if item is None:
            raise HTTPException(
                status_code=404, detail=f"Item Not Found(id: {item_id})",
            )
        
        await session.delete(item) 
        await session.commit()
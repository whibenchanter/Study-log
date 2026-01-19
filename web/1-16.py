### 1-16.blocking.py ### 
#    (개념설명용)
# FASTAPI는 왜 빠를까?

import asyncio  # 비동기 처리 도구
import time  # 시간 관련 함수 (동기적 슬립)

async def async_sleep():  # 양보하는 코루틴함수(협동함수, 자녀)
    await asyncio.sleep(3)  # 3초 대기, 다른 작업 가능

async def blocking_sleep():  # 양보 못하게 막음
    time.sleep(3)  # 3초 동안 아무것도 못함 (블로킹)

async def main():  # 메인 함수

    coro1 = async_sleep()  # 코루틴 객체 생성
    coro2 = async_sleep()  # 코루틴 객체 생성

    await asyncio.gather(coro1, coro2)  # 여러작업 묶어주는 도구

asyncio.run(main())  # 이벤트루프 실행 (순서관리자, 엄마) 
# 이벤트루프(순서관리자, 엄마) 
# 실행 중(한번에 1개씩, line23), 
# 대기 중(I/O 작업 중, line10),  
# 준비 중(I/O 작업완료 이후, line10에서 3초 지난 이후)











### 1-16.model.py ###
# 모델링(설계도)
from sqlalchemy import Integer, String  # 데이터 타입 정의용
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column  # ORM 도구


class Base(DeclarativeBase):  # 모든 모델의 부모 클래스
    pass


class Item(Base):  # Item 테이블 정의
    __tablename__ = "items"  # 실제 DB 테이블 이름
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # 기본키, 자동증가
    name: Mapped[str] = mapped_column(String(100), nullable=False)  # 상품명, 필수
    price: Mapped[int] = mapped_column(Integer, nullable=False)  # 가격, 필수











### 1-16.connection_async.py ###
# (국토교통부에서 관리하는 고속도로 생성 = 연결 + 관리)

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession  # 비동기 DB 엔진
from sqlalchemy.orm import sessionmaker  # 세션 공장 생성용

# 주소
DATABASE_URL = "sqlite+aiosqlite:///./test.db"  # SQLite 비동기 주소

# 편도 = 주소로 가는 길
engine = create_async_engine(DATABASE_URL)  # DB 엔진 생성

# 세션공장(설계도) (* 세션(Session) = DB 연결 및 도로관리차량)
AsyncSessionFactory = sessionmaker(  # 세션 공장 설정
    bind=engine,  # 엔진 연결
    class_=AsyncSession,  # 비동기 세션 사용
    autocommit=False,  # 자동 커밋 끄기
    autoflush=False,  # 자동 플러시 끄기
    expire_on_commit=False,  # 커밋 후 만료 끄기
)

# DB 연결 및 도로관리차량투입 및 해제 
async def get_async_session():  # 투입할 애들 만들기
    async with AsyncSessionFactory() as session:  # 세션 생성
        yield session  # 관리 끝나면 실행 = 연결 해제









### 1-16.crud_async.py ### 
#          (실행부)

# 필요 패키지 설치
# aiosqlite: SQLite용 비동기 드라이버
# greenlet: SQLAlchemy 비동기 기능을 위한 필수 의존성
# pip install aiosqlite
# pip install greenlet
from fastapi import FastAPI, HTTPException, status, Depends  # FastAPI 및 HTTP 에러 처리
from pydantic import BaseModel  # 데이터 검증용 모델
from sqlalchemy import select  # SQL SELECT 문 생성용

from connection_async import AsyncSessionFactory, get_async_session  # DB 연결 가져오기
# 위의 파일 연결하는 코드
from model import Item  # Item 모델 가져오기
# 위의 파일 연결하는 코드2

app = FastAPI()  # 앱 생성

class ItemResponse(BaseModel):  # 응답용 데이터 형식
    id: int  # 상품 ID
    name: str  # 상품명
    price: int  # 가격

# C: 상품 등록 API
class ItemCreateRequest(BaseModel):  # 생성 요청용 데이터 형식
    name: str  # 상품명
    price: int  # 가격

#의존성 주입(Dependency Injection) 적용한 버전
@app.post("/items", status_code=201)  # POST /items, 성공시 201 반환
async def create_item_api(
    body: ItemCreateRequest,  # 요청 바디
    session: AsyncSession = Depends(get_async_session),  # get_async_session 주입
) -> ItemResponse:  # 반환 타입
    new_item = Item(name=body.name, price=body.price)  # 새 아이템 생성
    session.add(new_item)  # DB에 저장할 애들을 선별
    await session.commit()  # DB에 반영
    return new_item  # 생성된 아이템 반환

# R: 전체 상품 조회 API
@app.get("/items", status_code=200)  # GET /items
async def get_items_api() -> list[ItemResponse]:  # 리스트 반환
    async with AsyncSessionFactory() as session:  # 세션 열기
        stmt = select(Item)  # statement = SQL 구문
        result = await session.execute(stmt)  # 1) DB 조회
        items : list[Item]= result.scalars().all()  # 2) Item 객체로 변환
        return items  # 전체 아이템 반환

# R: 단일 상품 조회 API
@app.get("/items/{item_id}", status_code=200)  # GET /items/{id}
async def get_item_api(item_id: int) -> ItemResponse:  # 단일 아이템 반환
    async with AsyncSessionFactory() as session:  # 세션 열기
        stmt = select(Item).where(Item.id == item_id)  # ID로 필터링
        result = await session.execute(stmt)  # DB 조회
        item: Item | None = result.scalar()  # 결과 추출
        
        if item is None:  # 없으면
            raise HTTPException(  # 404 에러 발생
                status_code=404, detail=f"Item Not Found(id: {item_id})",
            )
        return item  # 찾은 아이템 반환

# U: 상품 수정 API (PATCH) - 부분 수정
class ItemUpdateRequest(BaseModel):  # 수정 요청용
    name: str | None = None  # 선택적
    price: int | None = None  # 선택적

@app.patch("/items/{item_id}", status_code=200)  # PATCH 메서드
async def update_item_api(item_id: int, body: ItemUpdateRequest) -> ItemResponse:
    async with AsyncSessionFactory() as session:  # 세션 열기
        stmt = select(Item).where(Item.id == item_id)  # ID로 찾기
        result = await session.execute(stmt)  # DB 조회
        item: Item | None = result.scalar()  # 결과 추출
        
        if item is None:  # 없으면 404
            raise HTTPException(
                status_code=404, detail=f"Item Not Found(id: {item_id})",
            )
        
        if body.name:  # 이름이 있으면
            item.name = body.name  # 이름 수정
        if body.price:  # 가격이 있으면
            item.price = body.price  # 가격 수정
        
        await session.commit()  # DB 반영
        return item  # 수정된 아이템 반환

# U: 상품 수정 API (PUT) - 전체 교체
class ItemReplaceUpdate(BaseModel):  # 교체 요청용
    name: str  # 필수
    price: int  # 필수

@app.put("/items/{item_id}", status_code=200)  # PUT 메서드
async def replace_item_api(item_id: int, body: ItemReplaceUpdate) -> ItemResponse:
    async with AsyncSessionFactory() as session:  # 세션 열기
        stmt = select(Item).where(Item.id == item_id)  # ID로 찾기
        result = await session.execute(stmt)  # DB 조회
        item: Item | None = result.scalar()  # 결과 추출
        
        if item is None:  # 없으면 404
            raise HTTPException(
                status_code=404, detail=f"Item Not Found(id: {item_id})",
            )
        
        item.name = body.name  # 이름 교체
        item.price = body.price  # 가격 교체
        
        await session.commit()  # DB 반영
        await session.refresh(item)  # 최신 데이터로 새로고침
        return item  # 교체된 아이템 반환


# D: 상품 삭제 API
@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)  # DELETE, 204 반환
async def delete_item_api(item_id: int) -> None:  # 반환값 없음
    async with AsyncSessionFactory() as session:  # 세션 열기
        stmt = select(Item).where(Item.id == item_id)  # ID로 찾기
        result = await session.execute(stmt)  # DB 조회
        item: Item | None = result.scalar()  # 결과 추출
        
        if item is None:  # 없으면 404
            raise HTTPException(
                status_code=404, detail=f"Item Not Found(id: {item_id})",
            )
        
        await session.delete(item)  # 아이템 삭제
        await session.commit()  # DB 반영


# ============================================
# 📌 코드 흐름 요약
# ============================================
# 1. 비동기(async/await): 대기 중 다른 작업 처리 가능
# 2. SQLAlchemy ORM: 파이썬 객체로 DB 조작
# 3. 세션(Session): DB와의 연결 관리
# 4. CRUD 흐름:
#    - Create: session.add() → session.commit()
#    - Read: select() → session.execute() → result.scalar()
#    - Update: 객체 수정 → session.commit()
#    - Delete: session.delete() → session.commit()
# 5. HTTPException: 에러 발생시 404 등 상태코드 반환
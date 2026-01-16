from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# 데이터베이스 접속 정보 (async 버전은 aiosqlite 사용)
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# 엔진(Engine) = SQLAlchemy 사용시 DB와 연결관리
engine = create_async_engine(DATABASE_URL)

# 세션(Session) = DB 작업관리
# 세션을 만들 수 있는 세션 팩토리
AsyncSessionFactory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

# 추가한 부분
async def get_async_session(): # 주입할 애들 만들기
    async with AsyncSessionFactory() as session:
        yield session
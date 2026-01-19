# path_param.py
from fastapi import FastAPI, Path  # FastAPI 프레임워크, Path는 경로 파라미터 검증용


app = FastAPI()  # 앱 생성

# GET /items 요청시, root_api 함수를 실행한다.
@app.get("/items")  # GET 메서드로 /items 엔드포인트 정의
def root_api():  # 전체 아이템 목록 반환 함수
    return {  # 딕셔너리 형태로 응답
        "items": [  # 아이템 리스트
            {"id": 1, "name": "apple"},  # 사과
            {"id": 2, "name": "banana"},  # 바나나
            {"id": 3, "name": "cherry"}  # 체리
        ]
    }



# @app.get("/items/search") # 경로에서 표현하는건 자원임
# def item_api(): #int절로만 받겠다 (*타입강제고정 기능, str등도)
#     return {"msg": "search"}

# Path Parameter
# @app.get("/items/{item_id}") # 경로에서 표현하는건 자원임
# def item_api(item_id: int = Path(..., ge=1)): # ...은 필수값, ge=1은 1이상
#     return {"item": item_id}

# GET / items/{item_id}
# item_name: 문자열 & 최대 글자수(max_length) 4자
# 함수 : item_name 출력

@app.get('/items/{item_name}')  # 경로에 {item_name} = Path Parameter
def get_item(item_name: str = Path(..., max_length=6)):  # 필수값, 최대 6글자
    return {"item_name": item_name}  # 받은 이름 그대로 반환
















# query_param.py
from fastapi import FastAPI, Query  # Query는 쿼리 파라미터 검증용


app = FastAPI()  # 앱 생성

# Query Parameter
# ?{key}={value}
@app.get("/search")  # GET /search 엔드포인트
def search_api(q: str= Query(default='default', min_length=3, max_length=10)):  # 기본값 'default', 3~10글자
    return {"msg": f"search: {q}"}  # 검색어 반환

# GET /users/3/posts?limit=10 -> 3번 사용자의 게시물 10개를 조회
@app.get('/user/{user_id}/posts')  # Path + Query 함께 사용
def list_posts_api(user_id: int, limit: int):  # user_id는 Path, limit는 Query
   # Path -> 자원(리소스)을 식별
   # Query -> 조회 옵션
   
   # URL경로 상에 존재하면 Path, 없으면 Query
    return {'user_id': user_id, 'limit': limit}  # 둘 다 반환



















# 과제.py
    # 요구사항
# GET /products/search?q=apple&limit=5
# 응답
# {"q": "apple", "limit": 5}

from fastapi import FastAPI  # FastAPI 임포트
app = FastAPI()  # 앱 생성
@app.get('/products/search')  # GET /products/search 엔드포인트

def product_search(q: str = Query('apple'), limit: int = Query(..., ge=1)):  # q 기본값 'apple', limit 필수(1이상)
    return {"q": q, "limit": limit}  # 검색어와 개수 반환


# ============================================
# 📌 코드 흐름 요약
# ============================================
# 1. FastAPI 앱 생성 (app = FastAPI())
# 2. 엔드포인트 정의 (@app.get, @app.post 등)
# 3. Path Parameter: URL 경로에 포함 (/items/{item_name})
#    - 자원(리소스)을 식별할 때 사용
# 4. Query Parameter: URL 뒤에 ?key=value 형태
#    - 조회 옵션, 필터링에 사용
# 5. 요청이 오면 해당 함수 실행 → 응답 반환
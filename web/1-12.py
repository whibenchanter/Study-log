# path_param.py
from fastapi import FastAPI, Path


app = FastAPI()

# GET /hello 요청시, root_api 함수를 실행한다.
@app.get("/items")
def root_api():
    return {
        "items": [
            {"id": 1, "name": "apple"},
            {"id": 2, "name": "banana"},
            {"id": 3, "name": "cherry"}
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

@app.get('/items/{item_name}')
def get_item(item_name: str = Path(..., max_length=6)):
    return {"item_name": item_name}
















# query_param.py
from fastapi import FastAPI, Query


app = FastAPI()

# Query Parameter
# ?{key}={value}
@app.get("/search")
def search_api(q: str= Query(default='default', min_length=3, max_length=10)):
    return {"msg": f"search: {q}"}

# GET /users/3/posts?limit=10 -> 3번 사용자의 게시물 10개를 조회
@app.get('/user/{user_id}/posts')
def list_posts_api(user_id: int, limit: int): #limit값 안넣으면 3번 사용자의 게시물 전체조회
   # Path -> 자원(리소스)을 식별
   # Query -> 조회 옵션
   
   # URL경로 상에 존재하면 Path, 없으면 Query
    return {'user_id': user_id, 'limit': limit}



















# 과제.py
    # 요구사항
# GET /products/search?q=apple&limit=5
# 응답
# {"q": "apple", "limit": 5}

from fastapi import FastAPI
app = FastAPI()
@app.get('/products/search')

def product_search(q: str = Query('apple'), limit: int = Query(..., ge=1)):
    return {"q": q, "limit": limit}
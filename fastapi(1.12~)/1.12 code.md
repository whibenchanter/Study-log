# FastAPI 요약

## 1. Path Parameter (`path_param.py`)

### 기본 개념
- **Path Parameter**: URL 경로에서 **자원(Resource)**을 식별하는 값
- 형식: `/items/{item_id}` 에서 `{item_id}` 부분

### 주요 코드

```python
from fastapi import FastAPI, Path

app = FastAPI()

# 기본 GET 요청
@app.get("/items")
def root_api():
    return {"items": [{"id": 1, "name": "apple"}, ...]}

# Path Parameter 사용
@app.get('/items/{item_name}')
def get_item(item_name: str = Path(..., max_length=6)):
    return {"item_name": item_name}
```

### Path() 옵션
| 옵션 | 설명 |
|------|------|
| `...` | **필수값** (반드시 입력해야 함) |
| `ge=1` | 1 이상의 값만 허용 |
| `max_length` | 최대 문자 길이 제한 |

---

## 2. Query Parameter (`query_param.py`)

### 기본 개념
- **Query Parameter**: URL에서 **조회 옵션**을 지정하는 값
- 형식: `?key=value` (예: `/search?q=apple&limit=10`)

### Path vs Query 구분법
| 구분 | 위치 | 용도 |
|------|------|------|
| **Path** | URL 경로 안에 존재 | 자원(리소스) 식별 |
| **Query** | `?` 뒤에 존재 | 조회 옵션 지정 |

### 주요 코드

```python
from fastapi import FastAPI, Query

app = FastAPI()

# Query Parameter 기본 사용
@app.get("/search")
def search_api(q: str = Query(default='default', min_length=3, max_length=10)):
    return {"msg": f"search: {q}"}

# Path + Query 조합
# GET /users/3/posts?limit=10 → 3번 사용자의 게시물 10개 조회
@app.get('/user/{user_id}/posts')
def list_posts_api(user_id: int, limit: int):
    return {'user_id': user_id, 'limit': limit}
```

### Query() 옵션
| 옵션 | 설명 |
|------|------|
| `default` | 기본값 설정 |
| `min_length` | 최소 문자 길이 |
| `max_length` | 최대 문자 길이 |

---

## 3. 과제 예제 (`과제.py`)

### 요구사항
- **엔드포인트**: `GET /products/search?q=apple&limit=5`
- **응답**: `{"q": "apple", "limit": 5}`

### 구현 코드

```python
from fastapi import FastAPI

app = FastAPI()

@app.get('/products/search')
def product_search(q: str, limit: int = 10):
    return {"q": q, "limit": limit}
```

### 포인트
- `q: str` → 필수 Query Parameter
- `limit: int = 10` → 선택적 Query Parameter (기본값: 10)

---

## 핵심 정리

```
📌 Path Parameter  → URL 경로에 포함 → 자원 식별
📌 Query Parameter → ?key=value 형태 → 조회 옵션
```

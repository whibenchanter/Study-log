import asyncio  # 비동기 처리 도구

from llama_cpp import Llama  # AI 모델 로드용
from fastapi import FastAPI, Body  # 웹 서버 프레임워크
from fastapi.responses import StreamingResponse  # 스트리밍 응답용


# 모델 로드
llm = Llama(
    model_path="./models/Llama-3.2-1B-Instruct-Q4_K_M.gguf",  # 모델 파일 경로
    n_ctx=4096,  # 컨텍스트 길이(기억할 수 있는 글자 수)
    n_threads=2,  # CPU 스레드 수
    verbose=False,  # 디버그 출력 끔
    chat_format="llama-3",  # 대화 형식
)

# 시스템 프롬프트
SYSTEM_PROMPT = (
    "You are a concise assistant. "  # 간결한 도우미
    "Always reply in the same language as the user's input. "  # 사용자 언어로 답변
    "Do not change the language. "  # 언어 변경 금지
    "Do not mix languages."  # 언어 혼용 금지
)


app = FastAPI()  # 앱 생성

@app.post("/chats")  # POST /chats 엔드포인트
async def generate_chat_api(user_input: str = Body(...)):  # 사용자 입력 받음
    async def event_generator():  # 스트리밍 제너레이터
        response = llm.create_chat_completion(  # AI에게 요청
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},  # 시스템 지시
                {"role": "user", "content": user_input},  # 사용자 메시지
            ],
            max_tokens=256,  # 최대 토큰 수
            temperature=0.6,  # 창의성/자유도(0 ~ 1)
            stream=True,  # 스트리밍 모드
        )
        for chunk in response:  # 응답 청크 순회
            token = chunk["choices"][0]["delta"].get("content")  # 토큰 추출
            if token:
                yield token  # 토큰 전송
                await asyncio.sleep(0)  # 이벤트 루프 양보

    return StreamingResponse(
        event_generator(), media_type="text/event-stream"  # 스트리밍 응답
    )

    # curl -N -X POST http://127.0.0.1:8000/chats \ -H 
    # "Content-Type: application/json" \ -d '"너의 2026년 
    # 계획을 월별로 알려줘"'
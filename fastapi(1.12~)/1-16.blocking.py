import asyncio
import time


async def async_sleep():
    await asyncio.sleep(3)

async def blocking_sleep(): #양보 못하게 막음
    time.sleep(3)

async def main():
    coro1 = async_sleep()
    coro2 = async_sleep()
    
    await asyncio.gather(coro1, coro2) #여러작업 묶어주는 도구

asyncio.run(main()) #이벤트루프(순서관리자, 엄마 <-> 자녀 : 코루틴(중간에 멈췄다가 다시 이어서 실행할수 있는 협력함수))

# 실행 중(한번에 1개씩), 대기 중(I/O 작업 중),  준비 중(I/O 작업완료)
# ~~~~~~~~~~~~~~~...